const vscode = require("vscode");
const { execFile } = require("child_process");
const path = require("path");
const fs = require("fs");

const STAGED_DECORATION_SCHEME = "explorer-staged-tree";

const IGNORED_DIRS = new Set([
  ".git",
  "node_modules",
  ".venv",
  "venv",
  "__pycache__",
  ".pytest_cache",
  ".mypy_cache",
  ".ruff_cache",
  ".nuxt",
  ".output",
  ".cache",
  ".tox",
]);

/**
 * Runs a git command in `cwd` and returns trimmed stdout (or "" on error).
 * @param {string} cwd
 * @param {string[]} args
 * @param {number} [timeout=2500]
 * @returns {Promise<string>}
 */
function runGit(cwd, args, timeout = 2500) {
  return new Promise((resolve) => {
    execFile(
      "git",
      ["-c", "core.quotePath=false", ...args],
      { cwd, timeout, maxBuffer: 10 * 1024 * 1024 },
      (err, stdout) => {
        if (err || typeof stdout !== "string") {
          resolve("");
          return;
        }
        resolve(stdout.replace(/\r?\n$/, ""));
      }
    );
  });
}

/**
 * Resolves the REAL git directory of a working tree.
 * For a git worktree / submodule, `.git` is a plain file pointing elsewhere,
 * so the index we must watch lives outside the workspace folder.
 * @param {string} rootPath
 * @returns {Promise<string|null>}
 */
async function resolveGitDir(rootPath) {
  const gitDir = await runGit(rootPath, ["rev-parse", "--absolute-git-dir"], 2000);
  if (!gitDir) {
    return null;
  }
  try {
    return fs.statSync(gitDir).isDirectory() ? gitDir : null;
  } catch (_) {
    return null;
  }
}

/**
 * Watches the git index of every workspace folder and calls `onChange` whenever
 * it moves (`git add`, `git reset`, `git commit`, ...), no matter which terminal
 * or tool did it.
 * flow: rewire -> resolve git dirs -> fs.watch each dir + mtime poll as fallback
 * @param {() => void} onChange
 */
function createGitIndexWatcher(onChange) {
  const POLL_MS = 500;
  const WATCHED_NAMES = /^(index|index\.lock|HEAD|ORIG_HEAD|MERGE_HEAD|FETCH_HEAD)$/;

  /** @type {fs.FSWatcher[]} */
  let watchers = [];
  /** @type {string[]} */
  let gitDirs = [];
  /** @type {Map<string, number>} */
  const seenMtimes = new Map();
  let pollTimer = null;
  let disposed = false;
  let lastRewireTime = 0;

  function indexMtime(gitDir) {
    try {
      const idxPath = path.join(gitDir, "index");
      return fs.existsSync(idxPath) ? fs.statSync(idxPath).mtimeMs : 0;
    } catch (_) {
      return 0;
    }
  }

  // fs.watch can miss events on some filesystems, so poll the index mtime too
  async function pollOnce() {
    const now = Date.now();
    // Auto-detect git repo if not found at start or every 4s
    if (gitDirs.length === 0 || now - lastRewireTime > 4000) {
      lastRewireTime = now;
      await rewire();
    }
    for (const gitDir of gitDirs) {
      const mtime = indexMtime(gitDir);
      if (seenMtimes.get(gitDir) !== mtime) {
        seenMtimes.set(gitDir, mtime);
        onChange();
      }
    }
  }

  function closeWatchers() {
    for (const watcher of watchers) {
      try {
        watcher.close();
      } catch (_) {}
    }
    watchers = [];
  }

  async function rewire() {
    if (disposed) {
      return;
    }
    closeWatchers();
    seenMtimes.clear();

    const folders = vscode.workspace.workspaceFolders || [];
    const resolved = await Promise.all(
      folders.map((wf) => resolveGitDir(wf.uri.fsPath))
    );
    gitDirs = Array.from(new Set(resolved.filter(Boolean)));

    for (const gitDir of gitDirs) {
      seenMtimes.set(gitDir, indexMtime(gitDir));
      try {
        // `git add` writes index.lock then renames it onto index -> "rename" event
        const watcher = fs.watch(gitDir, (_event, fileName) => {
          if (!fileName || WATCHED_NAMES.test(String(fileName))) {
            onChange();
          }
        });
        watcher.on("error", () => {});
        watchers.push(watcher);
      } catch (_) {}
    }
  }

  rewire();
  pollTimer = setInterval(pollOnce, POLL_MS);

  return {
    rewire,
    dispose() {
      disposed = true;
      if (pollTimer) {
        clearInterval(pollTimer);
        pollTimer = null;
      }
      closeWatchers();
    },
  };
}

/**
 * Lists ONLY staged (`git add`) files via `git diff --cached --name-status`.
 * @param {string} rootPath
 * @returns {Promise<Array<{ relPath: string, fullPath: string, status: string }>>}
 */
async function listWorkspaceStagedFiles(rootPath) {
  const stdout = await runGit(rootPath, ["diff", "--cached", "--name-status"]);
  if (!stdout) {
    return [];
  }
  const results = [];
  const lines = stdout.split(/\r?\n/);
  for (const rawLine of lines) {
    if (!rawLine) {
      continue;
    }
    const parts = rawLine.split("\t");
    if (parts.length < 2) {
      continue;
    }
    const status = (parts[0] || "M").trim().charAt(0) || "M";
    let relPath = parts[parts.length - 1].trim();
    if (relPath.startsWith('"') && relPath.endsWith('"')) {
      relPath = relPath.slice(1, -1);
    }
    if (!relPath || relPath.endsWith("/")) {
      continue;
    }
    const fullPath = path.join(rootPath, relPath);
    results.push({
      relPath,
      fullPath,
      status,
    });
  }
  return results;
}

/**
 * Checks whether a file has tracked Git changes in the working tree / index.
 * @param {string} fsPath
 * @returns {Promise<boolean>}
 */
async function isGitModifiedTrackedFile(fsPath) {
  const cwd = path.dirname(fsPath);
  const statusOut = (
    await runGit(cwd, ["status", "--porcelain", "--", fsPath], 1000)
  ).trim();
  if (!statusOut) {
    return false;
  }
  const firstLine = statusOut.split(/\r?\n/)[0].trim();
  if (
    !firstLine ||
    firstLine.startsWith("??") ||
    firstLine.startsWith("!!")
  ) {
    return false;
  }
  return true;
}

/**
 * Sorts children so folders appear first (alphabetically), followed by files (alphabetically).
 */
function sortTreeNodes(nodes) {
  return nodes.sort((a, b) => {
    if (a.type !== b.type) {
      return a.type === "folder" ? -1 : 1;
    }
    return a.name.localeCompare(b.name);
  });
}

class FullProjectStagedTreeProvider {
  constructor(decorationEmitter) {
    this._onDidChangeTreeData = new vscode.EventEmitter();
    this.onDidChangeTreeData = this._onDidChangeTreeData.event;
    this._decorationEmitter = decorationEmitter;
    this.treeView = null;
    /** @type {Map<string, { status: string, relPath: string, rootPath: string }>} */
    this.stagedFiles = new Map();
    /** @type {Map<string, number>} */
    this.stagedFolderCounts = new Map();
  }

  async refresh() {
    await this.refreshStagedState();
    this._onDidChangeTreeData.fire(undefined);
    if (this._decorationEmitter) {
      this._decorationEmitter.fire(undefined);
    }
  }

  async refreshStagedState() {
    const folders = vscode.workspace.workspaceFolders;
    const nextStagedFiles = new Map();
    const nextStagedFolderCounts = new Map();
    let totalStaged = 0;

    if (folders && folders.length > 0) {
      for (const wf of folders) {
        const rootPath = wf.uri.fsPath;
        const stagedList = await listWorkspaceStagedFiles(rootPath);
        totalStaged += stagedList.length;

        for (const item of stagedList) {
          nextStagedFiles.set(item.fullPath, {
            status: item.status,
            relPath: item.relPath,
            rootPath,
          });

          // Walk up parent directories up to rootPath so every ancestor folder gets marked & auto-expanded
          let dir = path.dirname(item.fullPath);
          while (dir && dir.startsWith(rootPath)) {
            nextStagedFolderCounts.set(
              dir,
              (nextStagedFolderCounts.get(dir) || 0) + 1
            );
            if (dir === rootPath) {
              break;
            }
            const parent = path.dirname(dir);
            if (parent === dir) {
              break;
            }
            dir = parent;
          }
        }
      }
    }

    this.stagedFiles = nextStagedFiles;
    this.stagedFolderCounts = nextStagedFolderCounts;

    if (this.treeView) {
      this.treeView.description =
        totalStaged > 0
          ? `🟢 ${totalStaged} file git add`
          : "Chưa có file git add";
    }
  }

  /**
   * Reads a single directory level on disk and merges any staged-deleted files.
   * @param {string} dirPath
   * @param {string} rootPath
   */
  readDirectoryChildren(dirPath, rootPath) {
    const childrenMap = new Map();

    try {
      const dirents = fs.readdirSync(dirPath, { withFileTypes: true });
      for (const dirent of dirents) {
        const name = dirent.name;
        if (IGNORED_DIRS.has(name)) {
          continue;
        }
        const fullPath = path.join(dirPath, name);
        const relPath = path
          .relative(rootPath, fullPath)
          .split(path.sep)
          .join("/");

        if (dirent.isDirectory()) {
          childrenMap.set(fullPath, {
            type: "folder",
            name,
            relPath,
            fullPath,
            rootPath,
          });
        } else if (dirent.isFile() || dirent.isSymbolicLink()) {
          childrenMap.set(fullPath, {
            type: "file",
            name,
            relPath,
            fullPath,
            rootPath,
          });
        }
      }
    } catch (_) {}

    // Also include any staged deleted file (`git rm` / deleted then `git add`) in this directory
    for (const [stagedFullPath, info] of this.stagedFiles.entries()) {
      if (
        path.dirname(stagedFullPath) === dirPath &&
        !childrenMap.has(stagedFullPath)
      ) {
        childrenMap.set(stagedFullPath, {
          type: "file",
          name: path.basename(stagedFullPath),
          relPath: info.relPath,
          fullPath: stagedFullPath,
          rootPath: info.rootPath,
        });
      }
    }

    return sortTreeNodes(Array.from(childrenMap.values()));
  }

  getParent(element) {
    if (!element || !element.fullPath || !element.rootPath) {
      return null;
    }
    const parentPath = path.dirname(element.fullPath);
    if (
      !parentPath ||
      parentPath === element.fullPath ||
      parentPath === element.rootPath ||
      !parentPath.startsWith(element.rootPath)
    ) {
      return null;
    }
    const relPath = path
      .relative(element.rootPath, parentPath)
      .split(path.sep)
      .join("/");
    return {
      type: "folder",
      name: path.basename(parentPath),
      relPath,
      fullPath: parentPath,
      rootPath: element.rootPath,
    };
  }

  async getChildren(element) {
    const folders = vscode.workspace.workspaceFolders;
    if (!folders || folders.length === 0) {
      return [];
    }

    if (!element) {
      await this.refreshStagedState();
      if (folders.length === 1) {
        const rootPath = folders[0].uri.fsPath;
        return this.readDirectoryChildren(rootPath, rootPath);
      }
      return folders.map((wf) => ({
        type: "folder",
        name: wf.name,
        relPath: wf.name,
        fullPath: wf.uri.fsPath,
        rootPath: wf.uri.fsPath,
      }));
    }

    if (element.type === "folder") {
      return this.readDirectoryChildren(element.fullPath, element.rootPath);
    }

    return [];
  }

  getTreeItem(element) {
    if (element.type === "folder") {
      const stagedCount = this.stagedFolderCounts.get(element.fullPath) || 0;
      const hasStaged = stagedCount > 0;

      // Auto-expand folders that contain staged (`git add`) files; keep other folders collapsed
      const collapsibleState = hasStaged
        ? vscode.TreeItemCollapsibleState.Expanded
        : vscode.TreeItemCollapsibleState.Collapsed;

      const item = new vscode.TreeItem(element.name, collapsibleState);
      // Include open/closed state + staged count in ID so VS Code immediately updates badge & expands
      item.id = `folder:${element.fullPath}:${hasStaged ? `open:${stagedCount}` : "closed"}`;
      item.resourceUri = vscode.Uri.from({
        scheme: STAGED_DECORATION_SCHEME,
        path: element.fullPath,
        query: hasStaged ? `staged=${stagedCount}` : "",
      });

      if (hasStaged) {
        item.description = `🟢 git add (${stagedCount})`;
        item.iconPath = new vscode.ThemeIcon(
          "folder-opened",
          new vscode.ThemeColor("gitDecoration.addedResourceForeground")
        );
        item.tooltip = `${element.relPath} — Có ${stagedCount} file đã git add bên trong (Đã tự động xổ ra)`;
      } else {
        item.description = "";
        item.iconPath = vscode.ThemeIcon.Folder;
        item.tooltip = element.relPath;
      }

      return item;
    }

    // File item
    const stagedInfo = this.stagedFiles.get(element.fullPath) || null;
    const isStaged = Boolean(stagedInfo);
    const status = stagedInfo ? stagedInfo.status : "";

    const item = new vscode.TreeItem(
      element.name,
      vscode.TreeItemCollapsibleState.None
    );
    item.id = `file:${element.fullPath}:${isStaged ? status : "clean"}`;
    item.resourceUri = vscode.Uri.from({
      scheme: STAGED_DECORATION_SCHEME,
      path: element.fullPath,
      query: isStaged ? `status=${status}` : "",
    });

    if (isStaged) {
      item.description = `🟢 git add [${status}]`;
      item.iconPath = new vscode.ThemeIcon(
        "diff-added",
        new vscode.ThemeColor("gitDecoration.addedResourceForeground")
      );
      item.tooltip = `${element.relPath} — Đã git add [${status}] (Bấm để mở Git Diff)`;
    } else {
      item.description = "";
      item.iconPath = vscode.ThemeIcon.File;
      item.tooltip = element.relPath;
    }

    item.command = {
      command: "explorerDiffOnClick.openAndReveal",
      title: "Open Diff or File",
      arguments: [element],
    };
    return item;
  }
}

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
  let enabled = context.globalState.get("explorerDiffOnClick.enabled", true);
  let isConvertingTab = false;
  let lastActiveTabKind = null;
  let lastActiveFsPath = null;

  const decorationEmitter = new vscode.EventEmitter();
  const decorationProvider = {
    onDidChangeFileDecorations: decorationEmitter.event,
    provideFileDecoration(uri) {
      if (uri.scheme !== STAGED_DECORATION_SCHEME || !uri.query) {
        return undefined;
      }
      if (uri.query.startsWith("staged=")) {
        return new vscode.FileDecoration(
          "●",
          "Thư mục có chứa file đã git add",
          new vscode.ThemeColor("gitDecoration.addedResourceForeground")
        );
      }
      if (uri.query.startsWith("status=")) {
        const status = uri.query.slice("status=".length) || "M";
        return new vscode.FileDecoration(
          status.slice(0, 2),
          "File đã git add",
          new vscode.ThemeColor("gitDecoration.addedResourceForeground")
        );
      }
      return undefined;
    },
  };

  const decorationRegistration =
    vscode.window.registerFileDecorationProvider(decorationProvider);

  const treeProvider = new FullProjectStagedTreeProvider(decorationEmitter);
  const treeView = vscode.window.createTreeView(
    "explorerDiffOnClick.changedFiles",
    {
      treeDataProvider: treeProvider,
      showCollapseAll: true,
    }
  );
  treeProvider.treeView = treeView;

  const statusBarItem = vscode.window.createStatusBarItem(
    vscode.StatusBarAlignment.Left,
    100
  );
  statusBarItem.command = "explorerDiffOnClick.toggle";

  function updateStatusBar() {
    statusBarItem.text = enabled
      ? "$(diff) Diff-on-Click: ON"
      : "$(diff) Diff-on-Click: OFF";
    statusBarItem.tooltip = enabled
      ? "Clicking a modified file opens Git Diff automatically (Click to disable)"
      : "Explorer Diff-on-Click is disabled (Click to enable)";
    statusBarItem.show();
  }

  updateStatusBar();

  // Automatically open & focus the Project + Staged Tree on the Right Sidebar
  setTimeout(() => {
    vscode.commands
      .executeCommand("explorerDiffOnClick.changedFiles.focus")
      .then(undefined, () => {});
  }, 600);

  const focusRightPanelCmd = vscode.commands.registerCommand(
    "explorerDiffOnClick.focusRightPanel",
    async () => {
      await vscode.commands.executeCommand(
        "explorerDiffOnClick.changedFiles.focus"
      );
    }
  );

  const togglePanelCmd = vscode.commands.registerCommand(
    "explorerDiffOnClick.togglePanel",
    async () => {
      if (treeView.visible) {
        await vscode.commands.executeCommand(
          "workbench.action.closeAuxiliaryBar"
        );
        return;
      }
      await vscode.commands.executeCommand(
        "explorerDiffOnClick.changedFiles.focus"
      );
      treeProvider.refresh();
    }
  );

  const toggleCmd = vscode.commands.registerCommand(
    "explorerDiffOnClick.toggle",
    async () => {
      enabled = !enabled;
      await context.globalState.update("explorerDiffOnClick.enabled", enabled);
      updateStatusBar();
      vscode.window.setStatusBarMessage(
        `Explorer Diff-on-Click: ${enabled ? "ON" : "OFF"}`,
        2500
      );
    }
  );

  const refreshCmd = vscode.commands.registerCommand(
    "explorerDiffOnClick.refresh",
    () => {
      treeProvider.refresh();
    }
  );

  const openAndRevealCmd = vscode.commands.registerCommand(
    "explorerDiffOnClick.openAndReveal",
    async (fileElement) => {
      if (!fileElement || !fileElement.fullPath) {
        return;
      }
      const uri = vscode.Uri.file(fileElement.fullPath);
      isConvertingTab = true;
      try {
        if (fs.existsSync(fileElement.fullPath)) {
          try {
            await vscode.commands.executeCommand("revealInExplorer", uri);
          } catch (_) {}
        }

        const isStaged = treeProvider.stagedFiles.has(fileElement.fullPath);
        const isModified =
          isStaged || (await isGitModifiedTrackedFile(fileElement.fullPath));

        if (isModified) {
          await vscode.commands.executeCommand("git.openChange", uri);
          lastActiveTabKind = "diff";
          lastActiveFsPath = fileElement.fullPath;
        } else if (fs.existsSync(fileElement.fullPath)) {
          await vscode.window.showTextDocument(uri, { preview: true });
          lastActiveTabKind = "text";
          lastActiveFsPath = fileElement.fullPath;
        }
      } catch (_) {
        try {
          if (fs.existsSync(fileElement.fullPath)) {
            await vscode.window.showTextDocument(uri, { preview: true });
          }
        } catch (__) {}
      } finally {
        isConvertingTab = false;
      }
    }
  );

  async function handleActiveTabChange() {
    if (isConvertingTab) {
      return;
    }

    const activeGroup = vscode.window.tabGroups.activeTabGroup;
    if (!activeGroup || !activeGroup.activeTab) {
      lastActiveTabKind = null;
      lastActiveFsPath = null;
      return;
    }

    const activeTab = activeGroup.activeTab;
    const input = activeTab.input;

    if (input instanceof vscode.TabInputTextDiff) {
      lastActiveTabKind = "diff";
      lastActiveFsPath =
        input.modified && input.modified.scheme === "file"
          ? input.modified.fsPath
          : null;
      return;
    }

    if (!(input instanceof vscode.TabInputText) || input.uri.scheme !== "file") {
      lastActiveTabKind = "other";
      lastActiveFsPath = null;
      return;
    }

    const currentFsPath = input.uri.fsPath;

    if (lastActiveFsPath === currentFsPath) {
      lastActiveTabKind = "text";
      return;
    }

    lastActiveTabKind = "text";
    lastActiveFsPath = currentFsPath;

    if (!enabled) {
      return;
    }

    const isModified = await isGitModifiedTrackedFile(currentFsPath);
    if (!isModified) {
      return;
    }

    const currentActiveTab = vscode.window.tabGroups.activeTabGroup?.activeTab;
    if (
      !currentActiveTab ||
      !(currentActiveTab.input instanceof vscode.TabInputText) ||
      currentActiveTab.input.uri.fsPath !== currentFsPath
    ) {
      return;
    }

    const plainTabToClose = !currentActiveTab.isDirty ? currentActiveTab : null;

    isConvertingTab = true;
    try {
      await vscode.commands.executeCommand("git.openChange", input.uri);
      lastActiveTabKind = "diff";
      lastActiveFsPath = currentFsPath;

      if (plainTabToClose) {
        const group = vscode.window.tabGroups.activeTabGroup;
        if (group) {
          const leftoverPlainTab = group.tabs.find(
            (t) =>
              t.input instanceof vscode.TabInputText &&
              t.input.uri.fsPath === currentFsPath &&
              !t.isDirty
          );
          const hasDiffTab = group.tabs.some(
            (t) =>
              t.input instanceof vscode.TabInputTextDiff &&
              t.input.modified.fsPath === currentFsPath
          );
          if (leftoverPlainTab && hasDiffTab) {
            await vscode.window.tabGroups.close(leftoverPlainTab, true);
          }
        }
      }
    } catch (_) {
    } finally {
      isConvertingTab = false;
    }
  }

  let refreshTimer = null;
  function scheduleRefresh() {
    if (refreshTimer) {
      clearTimeout(refreshTimer);
    }
    refreshTimer = setTimeout(() => {
      treeProvider.refresh();
    }, 80);
  }

  function hookBuiltinGit() {
    try {
      const gitExt = vscode.extensions.getExtension("vscode.git");
      if (!gitExt) {
        return;
      }
      const setupGitApi = () => {
        try {
          const gitApi = gitExt.exports?.getAPI ? gitExt.exports.getAPI(1) : null;
          if (!gitApi) return;

          const hookRepo = (repo) => {
            if (!repo || !repo.state) return;
            context.subscriptions.push(
              repo.state.onDidChange(() => {
                scheduleRefresh();
              })
            );
          };

          gitApi.repositories.forEach(hookRepo);
          context.subscriptions.push(gitApi.onDidOpenRepository(hookRepo));
          if (gitApi.onDidChangeState) {
            context.subscriptions.push(gitApi.onDidChangeState(() => scheduleRefresh()));
          }
        } catch (_) {}
      };

      if (gitExt.isActive) {
        setupGitApi();
      } else {
        gitExt.activate().then(setupGitApi, () => {});
      }
    } catch (_) {}
  }

  hookBuiltinGit();

  const gitIndexWatcher = createGitIndexWatcher(scheduleRefresh);

  context.subscriptions.push(
    decorationRegistration,
    statusBarItem,
    treeView,
    focusRightPanelCmd,
    toggleCmd,
    refreshCmd,
    openAndRevealCmd,
    togglePanelCmd,
    gitIndexWatcher,
    vscode.workspace.onDidChangeWorkspaceFolders(() => {
      gitIndexWatcher.rewire();
      scheduleRefresh();
    }),
    vscode.workspace.onDidSaveTextDocument(scheduleRefresh),
    vscode.workspace.onDidCreateFiles(scheduleRefresh),
    vscode.workspace.onDidDeleteFiles(scheduleRefresh),
    vscode.workspace.onDidRenameFiles(scheduleRefresh),
    vscode.window.onDidChangeWindowState((e) => {
      if (e.focused) {
        scheduleRefresh();
      }
    }),
    vscode.window.tabGroups.onDidChangeTabs(handleActiveTabChange),
    vscode.window.tabGroups.onDidChangeTabGroups(handleActiveTabChange),
    vscode.window.onDidChangeActiveTextEditor(handleActiveTabChange)
  );
}

function deactivate() {}

module.exports = {
  activate,
  deactivate,
};
