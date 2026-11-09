# Skill: coding-rules

Một file duy nhất (`SKILL.md`) gom **toàn bộ quy tắc code** user đã dặn qua quá trình làm
việc: đặt tên hàm/biến, tách hàm dài, comment `# flow:`, phạm vi sửa, recon ast-graph,
kỷ luật xác minh, guardrail project sb-v123, style commit.

## Cài theo từng runtime

| Runtime | Chép `SKILL.md` vào |
|---|---|
| **Claude Code** | `~/.claude/skills/coding-rules/SKILL.md` → gọi `/coding-rules` |
| **Antigravity** | `<repo>/.agent/skills/coding-rules/SKILL.md`, hoặc dán nội dung vào `AGENTS.md` của repo / Rules toàn cục trong Settings |
| **opencode** | `<repo>/.opencode/skills/coding-rules/SKILL.md` |
| **Codex** | `~/.codex/skills/coding-rules/SKILL.md` → gọi `$coding-rules` |
| **Cursor / Windsurf** | `.cursor/rules/coding-rules.mdc` / `.windsurfrules` |

```bash
# ví dụ Claude Code
mkdir -p ~/.claude/skills/coding-rules
cp SKILL.md ~/.claude/skills/coding-rules/

# ví dụ Antigravity trong một repo
mkdir -p <repo>/.agent/skills/coding-rules
cp SKILL.md <repo>/.agent/skills/coding-rules/
```

## Prompt để nhờ agent máy khác tự cài

> Tôi gửi kèm file `SKILL.md` — đây là rulebook code của tôi. Hãy chép nó vào đúng thư
> mục skill/rules của runtime bạn đang chạy (Claude Code → `~/.claude/skills/coding-rules/`,
> Antigravity → `.agent/skills/coding-rules/` của repo, Codex → `~/.codex/skills/coding-rules/`),
> rồi từ giờ **đọc và tuân thủ nó trước khi viết, sửa, refactor hay review bất kỳ đoạn
> code nào**. Khi luật trong đó đá nhau với thói quen mặc định của bạn thì luật trong đó
> thắng. Xong báo tôi đã đặt file ở đâu.

## Lưu ý về nguồn

Bộ nhớ riêng của Antigravity (`~/.gemini/antigravity/implicit/*.pb`) **bị mã hoá/nén,
không đọc được**, và `~/.gemini/antigravity/knowledge/` đang rỗng. File này dựng từ các
nguồn đọc được: `~/.claude/CLAUDE.md`, skill `change-name`, skill `review-git-diff`, 10
file `feedback-*.md` trong memory của Claude Code, và `CLAUDE.md`/`AGENTS.md` của repo
sb-v123. Nếu trong Antigravity còn Rules/Memories nào chưa có ở đây, mở panel Memories
copy ra rồi bổ sung vào `SKILL.md`.
