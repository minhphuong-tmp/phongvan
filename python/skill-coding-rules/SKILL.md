---
name: coding-rules
description: Toàn bộ quy tắc code của user (phuongtong / SendByte) — cách đặt tên hàm & biến, cách tách hàm dài, cách viết comment, phạm vi sửa, recon bằng ast-graph, kỷ luật xác minh, guardrail project sb-v123. Nạp skill này TRƯỚC khi viết, sửa, refactor hay review bất kỳ đoạn code nào. Dùng cho mọi runtime (Antigravity / Claude Code / Codex / opencode).
---

# Coding rules — rulebook của user

Đây là tập hợp những gì user đã dặn trong quá trình làm việc. Không phải "best practice
chung" — là **luật riêng của user**, có chỗ cố tình đi ngược convention phổ biến. Khi
luật ở đây đá nhau với thói quen mặc định của bạn, **luật ở đây thắng**.

**Thứ tự ưu tiên:** lệnh trực tiếp của user > file này > `AGENTS.md`/`CLAUDE.md` của repo
> mặc định của bạn.

---

## 0. Trước khi gõ phím — quy trình

### 0.1 Recon bằng ast-graph TRƯỚC, grep là lưới an toàn
Với **mọi** tác vụ code (tìm symbol, call chain, blast radius, routes, dead code,
"cái này định nghĩa/dùng ở đâu"):

1. Query **ast-graph** trước (`mcp__ast-graph__*`). Nếu tool đang *deferred* (chỉ thấy
   tên, chưa có schema) thì **nạp schema qua `ToolSearch` rồi gọi** — ma sát đó không
   phải cớ để nhảy thẳng sang grep.
2. ast-graph là **snapshot một thời điểm** → có thể stale, thiếu code/symbol vừa thêm.
   Không ra kết quả hoặc nghi stale → **fallback grep/ripgrep** trên cây làm việc thật.
3. **Không bao giờ kết luận "không tồn tại" chỉ dựa trên ast-graph rỗng.** Phải grep xác
   nhận trước khi khẳng định vắng mặt.

> Đa worktree: ast-graph chỉ index `sb-v123`, nhưng `sb-broadcast` và `sendbyte` là
> **cùng repo** khác branch → cùng kiến trúc, cùng symbol. Kết quả graph áp dụng cho cả
> ba. Chỉ vùng code branch đó tự sửa mới cần grep lại trong đúng worktree.

### 0.2 Xác nhận bug bằng dữ liệu thật, đừng suy diễn rồi sửa
Thấy triệu chứng lạ ở local **không** chứng minh có bug trong code — dev/prod có thể
chạy đúng (config webhook khác, payload thật khác).

- Xác nhận bug bằng **payload / log thật**, không bằng suy luận.
- Chẩn đoán **read-only** rồi **ĐỀ XUẤT**; chờ user gật đầu mới sửa code trên feature
  branch.
- User lưỡng lự → **revert ngay** phần sửa phỏng đoán, giữ branch của user sạch.
- Quay lại đúng mục tiêu user đang làm, đừng đi lạc vào hố thỏ mình tự đào.

> Nguyên văn user: *"từ từ hãng sửa, bạn sửa làm gì"*.

### 0.3 Việc không được tự làm
- **Không `git commit`, không `git push`.** Mọi thay đổi để nguyên uncommitted cho dev
  tự review.
- **Không `git add .` / `git add -A`.** Stage từng file đúng của feature:
  `git add <đúng-file>`.
- **Không tự dispatch event ra dịch vụ ngoài** (CE / customer-engagement, Slack, API
  khách hàng) — kể cả gọi task qua Django shell. Chuẩn bị lệnh rồi đưa user chạy.
- **Không gộp lệnh mutate DB với lệnh chạy task trong cùng một block.** Mỗi bước
  (xoá dedup → set DB → chạy task) là một snippet **riêng**; lệnh xoá/sửa DB chỉ chạy
  khi user nói rõ "chạy đi". Query read-only thì tự chạy thoải mái.
- **Không tự chạy e2e/playwright để tự chụp màn hình** cho mấy tweak UI/CSS nhỏ. Sửa từ
  reasoning + screenshot user gửi (`~/Pictures/Screenshots/`), để user tự verify. Chỉ tự
  lái browser khi user bảo.
- **Không commit URL tunnel vào repo.** Chỉ ghi vào file gitignored (`api/.env`), và nên
  để script tunnel tự inject lúc chạy. Config production không đụng tới.

---

## 1. Phạm vi sửa — tối thiểu, đúng trọng tâm

### 1.1 Minimal diff
Chỉ chạm đúng dòng / hàm / file trực tiếp giải quyết yêu cầu hiện tại. **Tuyệt đối không
tiện tay**: refactor, đổi tên file/hàm/biến ngoài phạm vi, format cả file, viết lại code
lân cận đang chạy ổn.

### 1.2 Không lan ra file ngoài phạm vi
Không tự ý sửa kèm `.agent/skills/*`, `.opencode/skills/*`, `Makefile`, `docs/*`,
migration cũ, config local khi không được yêu cầu trực tiếp.

### 1.3 Giữ working tree sạch
Không để lại script test tạm / file nháp untracked trong repo.

### 1.4 Sửa review comment thì chỉ đụng symbol của feature này
Reviewer bảo "đưa event name thành constant" → **chỉ** áp cho symbol mà MR này sinh ra.
Không hoist giá trị có sẵn của feature khác lên constant chung. Không thêm constant chết
(0 usage).

Kiểm tra: `git show origin/main:<file>` — symbol đã có trên `main` và thuộc feature khác
→ để yên. Mỗi constant mới phải grep ra chỗ dùng thật.

> Ca cụ thể (MR !669): tôi hoist 5 event có sẵn + thêm `EVENT_GMV_TRACKED` chết → user
> bác. Diff phình = review lâu + rủi ro đụng feature khác.

---

## 2. Đặt tên — HÀM / METHOD

**Triết lý một dòng:** *đặt tên theo thứ người đọc cần — hàm thì theo **OUTPUT** nó trả
về hoặc **HÀNH ĐỘNG CHÍNH**, biến thì theo **VAI TRÒ** của giá trị — không theo cơ chế
bên trong, không theo edge case, không theo cách nó được tính ra. Ưu tiên từ đơn giản,
phổ thông, cụ thể. Nhất quán giữa các file anh em. Nhưng đừng bao giờ giản lược mất một
trạng thái đang gánh nghĩa, và đừng đổi tên đang là contract.*

**F1. Đặt theo OUTPUT trả về, hoặc HÀNH ĐỘNG CHÍNH** — không theo một bước nội bộ hay
edge case nó cũng xử lý.
- ✅ `build_email_content` ← `resolve_content`
- ✅ `get_recipients` ← `resolve_recipients`
- ✅ `render_token` ← `resolve_token`
- ✅ `get_recipient_timezone` ← `resolve_recipient_timezone`

**F2. Dùng động từ phổ thông, cụ thể:** `get`, `add`, `build`, `render`, `send`,
`capture`, `save`, `mark`, `count`. Tránh `resolve_` / `ensure_` / `handle_` /
`process_` / `do_` **khi có động từ cụ thể hợp hơn**.
- ✅ `add_unsubscribe_link` ← `ensure_unsubscribe_link`
- ✅ `capture_broadcast_block_images` ← `ensure_broadcast_block_images`
- ✅ `fail_broadcast_if_exhausted` rõ hơn `handle_failed_wave`

> User **cố ý** đánh đổi một chút chính xác lấy dễ đọc: dù `ensure_` *về mặt kỹ thuật*
> đúng (check-then-do, idempotent), user vẫn thích động từ hành động chính (`add_`,
> `capture_`). Gọi tên **hành động**, đừng gọi tên **cái chốt chặn**.

**F3. Nhất quán giữa anh em — cùng loại việc, cùng động từ.** Ba hàm anh em làm cùng một
kiểu việc thì đừng để một cái `send` còn hai cái `process_`.
- ✅ `send` / `send_gradual` / `send_recipient_local`

**F4. Tên KHOÁ — không đổi, không đề xuất đổi:**
- **Framework bắt:** resolver Graphene `resolve_<field>(self, info, …)`; override của
  `HTMLParser` (`handle_data` / `handle_starttag` / `handle_endtag`); dunder & hook của
  Django.
- **Hàm Celery task + chuỗi `name="…"`** — đổi là vỡ message đang nằm trong queue và
  beat schedule. (Đổi tên *service method* mà task gọi thì được.)
- **Động từ nghiệp vụ đúng nghĩa thì giữ.** `resolve_suspension` = "gỡ một suspension"
  (động từ nghiệp vụ thật, cặp với `has_unresolved_suspension`). `consume_send_quota` /
  `remaining_send_quota` — cặp từ vựng quota chuẩn, giữ.
- **Tên contract:** API public có caller ngoài, key của dict/config/return, cột CSV, field
  GraphQL. Hành vi và shape phải y nguyên.

**F5. Tên hàm/helper phải tự mô tả — dài mà rõ thì tốt.** Đọc tên là biết việc, không cần
mở thân hàm. Đừng rút ngắn để tiết kiệm ký tự nếu mất nghĩa.
- ✅ `_build_contact_field_to_csv_column_map`, `_verify_or_record_file_hash`,
  `_csv_row_to_contact_fields`, `_add_contacts_to_lists`, `_resolve_existing_status`;
  `parseHeaders`, `useImportTaskPolling`, `blockedByUsedSource`, `selectedDestination`
- ❌ `_proc`, `_handle2`, `doStuff`, `helper`, `_map`, `process`
- Tên = **động từ + tân ngữ** (`verb_noun` / `noun_to_noun` / `is_`/`has_`/`can_` cho
  boolean), không phải động từ trơ.

---

## 3. Đặt tên — BIẾN

**V1. Đặt theo VAI TRÒ / ý nghĩa của giá trị**, không theo phép tính sinh ra nó.
- ✅ `remaining_count`, `pending_contacts`, `audience_size`, `total_sent`

**V2. Lộ KIỂU/shape khi điều đó quan trọng** — collection vs count vs một phần tử.
- ✅ `remaining` → `remaining_count` (là số nguyên, không phải collection)
- ✅ `pending` → `pending_contacts` (là queryset)
- ✅ list id phải **số nhiều**: `contact_ids` — KHÔNG `contact_id` (đọc ra một id)

**V3. ĐỪNG giản lược mất TRẠNG THÁI / GIAI ĐOẠN đang gánh nghĩa.** Trạng thái mà giá trị
mang **chính là** "cái chính" — không phải chi tiết để bỏ. Giản lược ở đây không phải
dễ đọc hơn, mà là **đặt tên sai**.
- ❌ `attempted` → `sent` — giá trị có thể thành `sent` HOẶC `failed`; gọi là `sent` là
  nói dối ở nhánh thất bại
- ❌ `contacts_to_send` → `sent` — thời điểm đó chưa gửi gì cả
- ✅ giữ phân biệt `candidate_ids` vs `to_send`/đã dedup **khi thật sự có một bước
  dedup/transform** ở giữa

**V4. Boolean đọc như một câu hỏi / trạng thái.** Tiền tố `is_` / `has_` / `should_`.
- ✅ `has_next_wave`, `is_warm_up_run`, `is_subscribed` (← `consent`)

**V5. Độ dài tỉ lệ với phạm vi sống.** Biến vòng lặp ngắn hạn cứ ngắn (`c`, `item`); biến
sống cả hàm hoặc được return thì xứng đáng một cái tên đầy đủ (`send_this_wave`).

**V6. Đơn giản ≠ mơ hồ.** Cấm `data`, `result`, `val`, `tmp`, `info`, `obj`. Mục tiêu là
"ngắn gọn mà rõ vai trò", không phải "ngắn".

**V7. Python — collection là danh từ số nhiều, không Hungarian.**
- ✅ `contact_ids`, `pending_contacts`  ❌ `list_contact`, `list_pending_contact`

**V8. Nhất quán giữa các file anh em — cùng khái niệm, cùng tên.** Đây là kiểm tra có giá
trị cao nhất với biến. So logic song song giữa các file anh em rồi chỉnh cho khớp.
- ✅ `already` → `total_sent` (khớp file anh em đã dùng `total_sent`)
- ✅ `send_count` → `send_this_wave`; `contact_ids_to_send` → `contact_ids`;
  `throttled` (biến) → `has_next_wave` — đồng bộ qua mọi strategy
- Khi một cờ vừa là **biến** vừa là **key trả về**: chỉ đổi **biến**, giữ nguyên chuỗi
  key (`"throttled": has_next_wave`) trừ khi user đồng ý đổi cả contract.

**V9. Vừa đủ rõ** — thuật ngữ nghiệp vụ đã rõ thì để ngắn (`offset`, `batch`, `metrics`);
danh từ trơ mà mơ hồ thì thêm qualifier (`rows` → `csv_rows`, `field_map` →
`csv_field_mapping`, `lists` → `target_lists`). Đừng dài dòng vô ích. Áp cho **biến local
và tham số**.

---

## 4. Tách hàm dài & comment điều hướng

### 4.1 Tách hàm — mỗi mảnh phải xứng đáng tồn tại
Tách hàm **dài, nhiều bước** thành helper, mỗi helper làm **một bước có nghĩa** (lấy data
/ chia batch / upload S3).

**ĐỪNG tách quá tay** — hại ngang hàm khổng lồ:
- ❌ Không helper 1–3 dòng. Thân bước ngắn vậy thì để inline.
- ❌ Không wrapper pass-through (hàm chỉ gọi đúng một hàm khác). Inline nó.
- ❌ Không tách hàm vốn đã ngắn / đơn nhiệm chỉ để "cho gọn".
- Helper chỉ chính đáng khi nó ôm một khối logic thật VÀ bỏ nó ra khỏi hàm cha làm luồng
  của cha sáng hơn. Phân vân thì để inline.

> Vì sao: dõi logic qua một rừng hàm tí hon còn khó hơn đọc một hàm dài có nhãn.

### 4.2 Comment điều hướng — `# flow:` đánh số + nhãn bước + clarifier helper

Hàm đủ dài để giữ nhiều bước inline hoặc tách helper thì làm **đúng** như sau:

**(a) Đầu hàm orchestrator** — comment đánh số, **mỗi bước một dòng**, tiền tố `# N. `.
Sub-step thụt vào thành `# N.M`:
```python
# flow:
# 1. map columns
#    1.1 query the segment
#    1.2 query the lists
# 2. download file
# 3. guard file unchanged
# 4. upsert in batches
# 5. finalize
```
❌ Kiểu mũi tên cũ `# flow: map columns -> download file -> upsert` — **bỏ** từ
2026-07-05, vì mũi tên không mở rộng được cho sub-step.

**(b) Trên mỗi khối bước inline** — nhãn ngắn `# N. <step>`, số và từ khoá **khớp** một
dòng trong `# flow:` (`# 3. download file`). Thêm `: <ngắn gọn vì sao/làm gì>` chỉ khi
khối đó làm việc không hiển nhiên:
`# 3. guard file unchanged: ghi hash lần đầu, abort nếu lần resume thấy file khác`.

> ❌ **TUYỆT ĐỐI không** dùng nhãn `# step:` hay `# <step>` **không đánh số** trong thân
> hàm đã có `# flow:` — nó phá mapping giữa danh sách flow và khối code. Có `# flow:`
> đánh số thì **mọi** comment bước phải có tiền tố `# N.`.

**(c) Trên `def` của mỗi helper được tách ra** — `# N. <step>: <helper này làm gì>`.
Phần "làm gì" ngắn gọn ở đây là **được khuyến khích** (nó là biển chỉ đường, không phải
kể lể):
- ✅ `# 1. map columns: biến mỗi contact field thành một cột CSV đã chuẩn hoá`
- ✅ `# 2. get target lists: resolve id ra List object; không có thì về list mặc định`
- ✅ `# 5. upsert one batch: bỏ invalid/suppressed, update cái có sẵn, bulk-create cái mới`

### 4.3 Comment — theo loại file
- **Frontend (`.vue` / `.ts` / `.scss`):** không comment giải thích — cắt. Một nhãn
  section/component ngắn thì được (`<!-- List table -->`). FE để **tên rõ** làm việc.
- **Backend (`.py`):** nhiều nhất **một** dòng "vì sao" cho gotcha thật (resume-safety,
  thứ tự commit, quirk của hệ thống ngoài). Cắt mọi narration "cái gì".
- **Không docstring trong hàm.** Gỡ mọi `"""..."""` mô tả trong hàm mà diff thêm vào —
  kể cả khi hàm anh em có. Tên tự mô tả (F5) + biển chỉ đường `# flow:` đã nói hết ý
  định; docstring nhắc lại là thừa.
- **Tiếng Việt HOẶC tiếng Anh đều được** — tiếng Việt có dấu là ổn, **đừng** flag comment
  tiếng Việt là sai. Chọn **một** ngôn ngữ cho mỗi file và giữ nhất quán; code anh em
  xung quanh đang comment ngôn ngữ nào thì theo ngôn ngữ đó.
  (Luật "chỉ tiếng Anh" cũ đã **bỏ** từ 2026-07-05.)
- **Ngoại lệ được giữ:** các biển chỉ đường ở 4.2 (`# flow:`, `# N. <step>`,
  `# N. <step>: <làm gì>`) là **cấu trúc**, không phải narration → giữ, đừng cắt.

### 4.4 Cắt rác
Gọt chuỗi class Tailwind copy-paste xuống còn cái thật sự dùng; bỏ `console.log` và util
chết lọt vào diff.

---

## 5. Viết code vào file có sẵn — bám style của chính file đó

Viết hoặc refactor code vào một file thì theo **structure & style của CHÍNH file đó**,
không phải "best practice chung", để cả file đọc như một thể thống nhất.

> User từng bắt: *"sao các đoạn xung quanh gọn gàng lắm mà"*.

Trước khi sửa, quét pattern của file rồi soi gương:
- **Export visibility** — ví dụ `conditionFormatters.ts` để mọi formatter là
  `export const` thì cái mới cũng vậy.
- **Vị trí helper** — caller định nghĩa trước, helper nằm dưới (kiểu `formatCondition`
  → `formatTimeConstraint`).
- **Hình dáng control-flow** — case của `switch` `return` thẳng, chứ không
  `let x; x = ...; break`.
- Giữ hàm chính ngắn bằng cách đẩy phần phức tạp sang helper anh em, đúng cách file đó
  đang làm.
- Đừng format lại những dòng prettier đã wrap.

---

## 6. Tên & vị trí FILE mới

Chỉ xét **file mới** mà diff thêm vào (`git diff --name-status` status `A`, cộng untracked
`??`).

- **Tên:** flag tên mơ hồ hoặc phá convention của thư mục; tên đúng soi theo export chính
  hoặc các file anh em.
  > ✅ `helpers.ts` chứa GraphQL op của list/segment → `lists-segments.ts` (khớp anh em)
- **Vị trí:** xét theo (a) convention thư mục/anh em và (b) kiến trúc `.agent`.
  > ✅ composable viết thành `.ts` trong thư mục page → chuyển vào `composables/`;
  > helper dùng chung nằm cạnh page → `utils/`; component tái dùng nằm trong thư mục page
  > → `components/<feature>/`; business logic Django trong `views.py`/resolver →
  > `service/` / `services.py`
- Đổi tên/di chuyển thì phải **grep cả repo** theo basename cũ và sửa **mọi** chỗ import,
  không chỉ chỗ trong diff. Xong rồi grep lại — còn hit nào là import gãy.
- **Loại rủi ro — vẫn đề xuất nhưng CẢNH BÁO TO, user quyết:**
  - **File route/page:** đổi tên = **đổi URL** → đó là thay đổi hành vi/sản phẩm, không
    phải readability. Ghi `⚠️ URL đổi: …` và bắt user xác nhận rõ.
  - **Migration:** đổi tên là vỡ lịch sử migration của Django (migration khác
    `depends_on`, DB lưu tên đã apply). Ghi `⚠️ vỡ lịch sử migration` và khuyên đừng làm.
- **Tên convention/contract thì để yên, đừng nhắc tới.** Ví dụ đừng đổi
  `ContactImportService.run(task_id)` — `tasks.py` gọi nó và các anh em soi gương nó.

---

## 7. Quy trình review 3 pha (khi được nhờ review / đổi tên)

Luôn chạy **trong session này**, có người ở đó:

**Pha 1 — Tìm, KHÔNG sửa.**
1. **Liệt kê work-list trước.** Mọi biến và mọi hàm/method trong vùng mục tiêu (và file
   anh em nếu user chỉ cả module). Soi luật trên **danh sách này** — không nhìn áng chừng.
2. Đọc đủ ngữ cảnh để phán từng cái tên — hàm trả về gì / hành động chính là gì; biến giữ
   giá trị gì và có gánh trạng thái phải sống sót trong tên không (V3). Với file anh em,
   dóng hàng các biến song song để bắt V8.
3. Quét F1–F5 lên mọi hàm, V1–V9 lên mọi biến. Mỗi phát hiện thật → một cặp
   before→after cụ thể.
4. **Trình bày rồi DỪNG.** Danh sách đánh số, gom nhóm **Hàm (F)** rồi **Biến (V)**:
   ```
   N — <file>:<line>  [F1 output-name | V8 sibling-consistency | …]
     giờ:     <tên hiện tại + sai ở đâu>
     đề xuất: <old_name → new_name>
   ```
   Kết bằng đúng một câu hỏi: **"Đổi hết, hay chọn cái nào? (vd: 1,3,5 / 'hết' / 'bỏ 2')"**
   rồi **CHỜ**. Chưa sửa gì cả. Không có gì đáng đổi thì nói thẳng.

**Pha 2 — Áp (chỉ sau khi user duyệt).** Chỉ áp những mục được chấp nhận.
- Đổi **mọi chỗ xuất hiện** trong phạm vi: định nghĩa, mọi call-site, **tham số + argument
  ở call-site**, và các chỗ dùng lại sau (`x[-1]` kiểu con trỏ). Khớp theo word-boundary
  (`\bname\b`) để không đụng identifier dài hơn.
- **Giữ contract:** không đổi chuỗi key của dict/return, `name="…"` của task, chữ ký public
  mà caller phụ thuộc, hay hành vi của giá trị.
- **Không đụng comment / chuỗi log** chỉ vì nó chứa từ đó. `sed` toàn cục trên từ phổ
  thông (`wave`, `remaining`) sẽ băm nát văn xuôi.
- Grep lại tên CŨ trong cả vùng — còn sót (ngoài comment) là một tham chiếu bị bỏ lỡ.

**Pha 3 — Verify.**
1. Check cú pháp/compile file đã sửa (`python3 -m py_compile …`, hoặc lint/typecheck của
   project).
2. Grep tên cũ khắp module đã đụng — xác nhận 0 tham chiếu lạc (trừ comment/log, có thì
   ghi chú).
3. **Báo cáo** gọn: mỗi dòng một rename `old → new (file:line, luật)`, cộng
   `Bỏ qua / cần user quyết:` cho thứ còn treo, cộng lệnh verify + PASS/FAIL.

### Refactor ăn theo rename (chỉ khi nó làm một cái tên trở nên thừa)
- **Inline biến trung gian dùng đúng một lần** nếu nó không ghi dấu một bước riêng có
  nghĩa.
- **Giữ** biến được **dùng lại nhiều lần** hoặc ghi dấu một **bước có nghĩa** (vd
  `pending_contacts` dùng cho cả slice lẫn fetch; bước dedup khi nó bắc sang data store
  khác). Inline mấy cái đó là **giấu mất một bước thật**.
- **Không bao giờ gộp** một queryset với `.count()` của nó thành một biểu thức nếu
  queryset còn dùng lại — mất tham chiếu tái dùng và nhân đôi filter.

---

## 8. Guardrail project sb-v123 (SendByte Universe)

**B1. Chặn cứng — vi phạm là blocker, không phải nit.**
- **`api/sendbyte/email_ai/` là READ-ONLY.** Mọi sửa đổi bên trong đều bị cấm. Cần logic
  từ đó thì chuyển nó ra ngoài trước; đừng import trực tiếp từ `email_ai`.
- **Không cross-import.** `api/` **không được** import từ `app/` hay `sitekit/` (và ngược
  lại). Giao tiếp qua HTTP/gRPC.
- **Legacy vs modern.** Không trộn pattern Nuxt 4 / Vue 3 vào Vue 2
  (`sitekit/app/modules/`) và ngược lại. Coi là hai hệ sinh thái riêng.

**B2. Convention đặt tên file.** Python `snake_case.py`; Go/JS `camelCase` cho hàm/biến;
class `PascalCase`. **FE ghi đè luật kebab-case chung:** component `PascalCase.vue`,
composable/type/constant/store `camelCase.ts`, util `kebab-case.ts`, page `kebab` /
`[param]`. Đừng flag một component PascalCase là sai.

**B3. Shopify Polaris `s-*`.**
- Thuộc tính **camelCase**, không kebab: `minBlockSize` ✅ / `min-block-size` ❌.
- Dùng **thang có tên**, không token số: `gap="base"` ✅ / `gap="400"` ❌.
- **`s-box` không nhận `class`** — bọc `<div>` nếu cần class Tailwind.
- **`s-text` không nhận `class` / `variant`** — dùng `color`/`weight`/`tone`; heading dùng
  `<s-heading>`.
- Không còn tag `polaris-*`, chỉ `s-*`.
- Đừng gắn class Tailwind lên `s-*` vốn đã có prop styling.
- Modal: dashboard dùng shadcn `Dialog`/`AppModal` là chính — **đừng** flag nó là sai;
  toast dùng `vue-sonner`.

**B4. Django backend (`api/`).**
- Hàm/method mới phải có **type hint** (`def f(x: str) -> bool:`).
- **Business logic nằm ở `service/` / `services.py`**, không nằm trong view/resolver.
- GraphQL resolver là **wrapper mỏng** gọi service method.

**B5. Vee-validate + input `s-*`:** không `v-model` thẳng — dùng pattern sync thủ công
(`:value` + `@input`/`@change` → update store **và** `form.setFieldValue`).

**B6. Vị trí file (backend `api/sendbyte/<app>/`):**

| Việc | Nằm ở | Hình dáng |
|---|---|---|
| Route/URL, REST, webhook | `<app>/urls.py` + `views.py` (webhook public → `public_api/`) | `path()`/`include()` |
| Model / DB | `<app>/models.py` hoặc `models/<name>.py` | QuerySet/Manager đặt **trên** model trong cùng file |
| Query phức tạp | `<app>/query_services.py` hoặc `services/query_service.py` | `@staticmethod`; filter đơn giản để ở QuerySet/Manager. **Không ở resolver/view/model** |
| Business logic | `<app>/services.py` hoặc `services/<concern>_service.py` | class `XxxService`; job polling expose `.run(task_id)` |
| GraphQL | `<app>/schema/{query,mutation,type}.py` | resolver `resolve_<field>`, wrapper mỏng, `@authenticated`; input `XxxInput` |
| Celery task | `<app>/tasks.py` | `@shared_task(name="sendbyte.<app>.tasks.<fn>")`, động từ dẫn đầu, uỷ việc cho service |
| Pydantic schema | `<app>/schemas.py` | DTO, `model_dump()` / `model_validate()` |
| Test | `<app>/tests/test_*.py` | pytest |

**Frontend (`app/dashboard/layers/<layer>/`, alias `#<layer>`):**

| Việc | Nằm ở | Hình dáng |
|---|---|---|
| Component | `components/<feature>/Name.vue`; dùng chung → `components/shared/` | PascalCase; component tái dùng **không** nằm trong thư mục page |
| Page | `pages/apps/<app>/<feature>/...` (`[id].vue` = dynamic) | path = URL; page **chỉ điều phối**, không chứa business logic |
| Composable | `composables/useXxx.ts` | camelCase, tiền tố `use`; có `ref`/`computed`/lifecycle. Không có reactive state → đó là util |
| Store | `stores/<name>.ts` (Pinia) | chỉ dành cho global state thật (1–2 cái / layer) |
| GraphQL | const operation (`GET_X`) → `schema/<feature>.ts`; hook wrapper (`useXQuery`) → `graphql/<feature>.ts` | page/component dùng wrapper, **không** `gql` inline |
| Type | `types/<domain>.ts` | camelCase, chỉ type |
| Util thuần | `utils/<kebab>.ts` | kebab-case; không reactivity |
| Constant | `constants/<name>.ts` | camelCase |
| i18n | `i18n/locales/{en,vi,zh}.json` | mọi text người dùng thấy qua `$t()` — flag chuỗi hardcode |
| Style | Tailwind inline / `<style scoped>`; partial tái dùng → `assets/css/polaris-standalone/_<feature>.scss` | không tạo `.scss` riêng cho từng component |

**B7. Idiom backend sb-v123 — flag khi diff làm khác:**
- **Shape lỗi của mutation:** mutation chỉ validate → `raise ValidationError(...)`; mutation
  có side-effect (upsert/create có thể fail) → trả `{ success, message, data }`
  (`ValueError` → message cho user; `Exception` trần → log + message chung). Đừng để
  exception thô thoát ra từ mutation có side-effect.
- **Scope multi-tenant:** mọi query/mutation phải filter theo account/storefront của
  caller. Không thấy row → `ValidationError("… not found")`, **không bao giờ tiết lộ sự tồn
  tại** (không 403/"forbidden"). Query không scope theo account là lỗi.
- **`Task.state` có kiểu:** payload là Pydantic DTO trong `schemas.py` — ghi
  `state.model_dump()`, đọc `Model.model_validate(task.state or {})`,
  `ConfigDict(extra="ignore")`. Task state kiểu dict tự do là mùi lỗi.
- **Job dài (import/merge):** `transaction.atomic()` **theo từng batch**; checkpoint
  `state` + `progress` **ngoài** transaction bằng `save(update_fields=[…])`; `BATCH_SIZE`
  là class constant; job resume từ offset đã lưu. Vòng lặp dài không lưu gì (không
  resume được) hoặc bọc tất cả trong một transaction khổng lồ → flag.
- **Wrapper Celery:** claim status atomic (PENDING→RUNNING) để dedup + resume sau crash;
  task uỷ việc thật cho service `.run(task_id)`.
- **Event side-effect:** enqueue qua `transaction.on_commit(lambda: task.delay(…))`, không
  gọi inline trước commit (tránh bắn khi transaction bị rollback).
- **Log có cấu trúc:** `logger.info("msg", extra={…})` / structlog kwargs, không nội suy
  f-string.

**B8. Typing nghiêm.** Ép strong typing rõ ràng khắp monorepo. Tránh `any`, `as any`, tham
số không annotate, `dict[str, Any]` mà không có TypedDict/schema rõ.

**B9. Hợp đồng dữ liệu xuyên tầng (Anti-Miss Gate).** Thêm/sửa bất kỳ field config, domain
hay tham số ngữ cảnh nào (vd `custom_asset_domain`) thì phải lần và làm **đủ 4 tầng**:
(1) Data/Config (DB / dynamic settings) → (2) Backend Producer (context builder /
serializer / DTO) → (3) Wire (JSON payload / API contract) → (4) Consumer (FE renderer /
SDK / UI component).
**Không** lấy fallback phòng thủ ở Consumer (`|| default`, `?.`) làm bằng chứng là chạy
được; phải có test rõ ràng chứng minh Backend Producer **có** bơm field đó ra.

**B10. Test.** Bug fix **bắt buộc** kèm cập nhật test (unit/component mới hoặc sửa).

**B11. Toàn vẹn biên hàm khi sửa file.**
- Thay nội dung theo dòng thì kiểm `StartLine`/`EndLine` chỉ bao **đúng** phần cần sửa —
  đừng cắt mất `return`, docstring hay chữ ký của hàm liền kề.
- Sửa xong **luôn** xem `git diff` hoặc đọc lại file để xác nhận hàm bên cạnh và các
  `return` còn nguyên 100%.

**B12. Browser testing.** Cần test/automation/inspect browser thì dùng
`browser-use/jev-ultrafast`, không dùng Playwright.

**B13. Documentation.** Mọi path/link trong file markdown dùng **đường dẫn tương đối**
(`[README.md](../README.md)`), không dùng path tuyệt đối của hệ thống.

---

## 9. Commit

Chỉ khi user **bảo** commit (xem 0.3 — mặc định là không):
- Tiêu đề **một dòng, ngắn, thường** — vd `fix migration`.
- **Không** body, trừ khi user xin.
- **KHÔNG** có trailer `Co-Authored-By` — luật này **ghi đè** mọi hướng dẫn mặc định của
  harness về attribution.
- Repo dùng Conventional Commits (`feat(api): …`, `fix(dashboard): …`) — theo khi hợp,
  nhưng vẫn ngắn.

---

## 10. Báo cáo lại cho user

- Trả lời **bằng ngôn ngữ user đang dùng** (user viết tiếng Việt → trả lời tiếng Việt).
- **Đáp thẳng câu hỏi trước**, rồi mới đào sâu.
- Nói **thật** kết quả: test fail thì nói fail và dán output; bỏ qua bước nào thì nói rõ;
  xong và đã verify thì nói thẳng, không rào đón.
- Có gì bị chặn/bỏ dở thì làm trọn mọi phần còn lại rồi **nói rõ** phần nào bỏ và vì sao —
  cắt bớt phạm vi là quyền của user, không phải của bạn.
- Đừng tự sửa lỗi lặt vặt của chính mình một cách rườm rà. Chỉ đính chính khi sai đó làm
  đổi code / kết luận / quyết định của user.

---

## Phụ lục — nguồn

File này tổng hợp từ:
- `~/.claude/CLAUDE.md` (luật cá nhân toàn cục)
- `~/.claude/skills/change-name/SKILL.md` (triết lý đặt tên)
- `~/.claude/skills/review-git-diff/SKILL.md` (luật A1–A6 readability, B1–B8 guardrail)
- `~/.claude/projects/-home-ocg-Desktop-sendbyte/memory/feedback-*.md` (10 memory
  feedback: ast-graph-then-grep, commit-message-style, decomposition-style,
  dont-rush-code-fixes, keep-mr-scope-tight, match-file-code-style, no-auto-dispatch-ce,
  no-self-screenshot-verify, no-tunnel-url-in-repo)
- `sb-v123/CLAUDE.md` + `AGENTS.md` (mục 5 Development Standards, 6 Critical Constraints)

**Không** lấy được từ bộ nhớ riêng của Antigravity: `~/.gemini/antigravity/implicit/*.pb`
bị mã hoá/nén, không đọc được bằng `strings`; `~/.gemini/antigravity/knowledge/` rỗng
(chỉ có `knowledge.lock`). Nếu trong Antigravity bạn còn Rules/Memories nào chưa nằm ở
đây, mở panel Memories của nó copy ra rồi bổ sung vào file này.
