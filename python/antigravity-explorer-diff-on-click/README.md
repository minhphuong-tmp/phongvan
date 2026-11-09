# Explorer Diff on Click — v2.0.0

Extension tự viết cho **Antigravity** (hoặc VS Code / Cursor / Windsurf — cùng engine).

Nó dựng **cây thư mục toàn project ở Secondary Sidebar (bên phải)**, tự **xổ ra + tô
xanh** mọi file đã `git add` (staged), và click vào file sẽ mở thẳng **Git Diff** thay
vì mở file thường.

---

## Có gì mới ở 2.0.0

### 1. `Ctrl+R` = bật/tắt panel
- Panel đang hiện → `Ctrl+R` đóng Secondary Sidebar.
- Panel đang ẩn (hoặc sidebar đang hiện view khác) → `Ctrl+R` mở + focus vào panel này
  và refresh luôn.
- Command: `explorerDiffOnClick.togglePanel`.
- `Alt+G` (cũ) vẫn giữ: chỉ focus, không toggle.

> `Ctrl+R` mặc định của VS Code là **Open Recent**. Bản này giành phím đó. Nếu muốn trả
> lại, xoá 2 dòng `ctrl+r` trong `keybindings.json` (xem phần Cài đặt).

### 2. Tự reload khi `git add` — kể cả trong git worktree
Bản 1.9.0 theo dõi bằng glob `**/.git/{index,HEAD,refs/heads/**}`. Glob đó **chết trong
git worktree**: ở worktree, `.git` chỉ là một **file text** trỏ sang
`<repo-chính>/.git/worktrees/<tên>/`, nằm **ngoài** workspace folder → glob không bao giờ
khớp → watcher không bao giờ bắn → phải reload cả IDE mới thấy file vừa `git add`.

Bản 2.0.0 thay bằng `createGitIndexWatcher()`:
1. `git rev-parse --absolute-git-dir` cho **từng** workspace folder → ra git dir **thật**
   (đúng cả với worktree và submodule).
2. `fs.watch()` trên git dir đó — `git add` ghi `index.lock` rồi rename đè lên `index`,
   bắt được event `rename`.
3. Poll `mtime` của `index` mỗi 1 giây làm lưới an toàn (fs.watch rơi event trên một số
   filesystem / NFS / bind mount).
4. `onDidChangeWorkspaceFolders` → tự `rewire()` lại khi đổi/thêm folder.

Nghĩa là `git add` từ **terminal nào cũng được** — trong IDE, ngoài IDE, qua script —
panel tự cập nhật sau ~0.3–1s. Không cần bấm refresh, không cần reload window.

---

## Cài đặt

### Cách nhanh (có file .vsix)
```bash
antigravity --install-extension ./explorer-diff-on-click-2.0.0.vsix --force
```
(VS Code thì đổi `antigravity` → `code`; Cursor → `cursor`.)

Rồi **Reload Window** (`Ctrl+Shift+P` → `Developer: Reload Window`).

### Cách chắc ăn cho `Ctrl+R`
Extension đã khai báo `ctrl+r` trong `package.json`, nhưng để chắc chắn thắng phím mặc
định, thêm vào `keybindings.json` của IDE
(`Ctrl+Shift+P` → `Preferences: Open Keyboard Shortcuts (JSON)`):

```jsonc
{ "key": "ctrl+r", "command": "explorerDiffOnClick.togglePanel" },
{ "key": "ctrl+r", "command": "-workbench.action.openRecent" }
```

Dòng thứ hai (dấu `-` đằng trước) gỡ binding mặc định `Open Recent`.

### Cài từ source (không dùng .vsix)
```bash
mkdir -p ~/.config/antigravity-custom-extensions/explorer-diff-on-click
cp extension.js package.json icon.svg \
   ~/.config/antigravity-custom-extensions/explorer-diff-on-click/
```
Rồi đóng gói lại thành .vsix (xem `PROMPT-setup-antigravity-extension.md`) hoặc symlink
thẳng vào `~/.antigravity/extensions/local.explorer-diff-on-click-2.0.0/`.

---

## Dùng

| Thao tác | Kết quả |
|---|---|
| `Ctrl+R` | Bật / tắt panel "Project Tree (git add)" bên phải |
| `Alt+G` | Chỉ focus panel (không tắt) |
| Click file **đã staged** | Mở **Git Diff** của file đó |
| Click file thường | Mở file bình thường (preview) |
| Icon 🔄 trên title bar panel | Refresh thủ công |
| Status bar `Diff-on-Click: ON/OFF` | Bấm để bật/tắt chế độ tự chuyển tab file → tab diff |

Thư mục chứa file staged hiện `🟢 git add (N)` và **tự xổ ra**; file staged hiện
`🟢 git add [M|A|D|R]` kèm màu xanh của theme git.

Thư mục bị bỏ qua khi quét cây: `.git`, `node_modules`, `.venv`, `venv`, `__pycache__`,
`.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.nuxt`, `.output`, `.cache`, `.tox`
(sửa ở hằng `IGNORED_DIRS` đầu `extension.js`).

---

## File trong thư mục này

| File | Việc |
|---|---|
| `explorer-diff-on-click-2.0.0.vsix` | Gói cài sẵn — đem sang máy khác cài là chạy |
| `extension.js` | Toàn bộ logic |
| `package.json` | Manifest: view, command, keybinding |
| `icon.svg` | Icon panel |
