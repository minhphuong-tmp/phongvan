#!/usr/bin/env python3
import json
import html
import sys
from pathlib import Path

# Add scratch to sys.path
sys.path.insert(0, str(Path(__file__).parent))
from vue_data_1_50 import VUE_ANSWERS_PART1
from vue_data_51_100 import VUE_ANSWERS_PART2

VUE_ANSWERS_DB = {**VUE_ANSWERS_PART1, **VUE_ANSWERS_PART2}

def generate_vue_html():
    with open('/tmp/all_vue_questions.json', 'r', encoding='utf-8') as f:
        vue_questions = json.load(f)

    # Per user request: "vuejs đeer ở pythong nữa"
    out_dir = Path("/Users/macos/Desktop/phongvan/python")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "vuejs_interview_answers.html"
    root_mirror = Path("/Users/macos/Desktop/phongvan/vuejs_interview_answers.html")

    # Group by category
    cats = {}
    for q in vue_questions:
        c = q['category']
        if c not in cats: cats[c] = []
        cats[c].append(q)

    nav_html = []
    cards_html = []

    for cat_name, q_list in cats.items():
        cat_id = cat_name.lower().replace(" ", "-").replace("&amp;", "and").replace("&", "and")
        nav_html.append(f"""
        <div class="nav-cat-group">
            <a href="#{cat_id}" class="nav-cat-header">
                <span>{html.escape(cat_name)}</span>
                <span class="cat-count">{len(q_list)}</span>
            </a>
            <div class="nav-q-links">
        """)
        for q in q_list:
            nav_html.append(f"""
                <a href="#q-{q['id']}" class="nav-q-link">
                    <span class="q-num">Q{q['id']}</span>
                    <span class="q-sub">{html.escape(q['title'][:36])}...</span>
                </a>
            """)
        nav_html.append("</div></div>")

        cards_html.append(f"""
        <section id="{cat_id}" class="cat-section">
            <div class="cat-section-header">
                <h2>💚 {html.escape(cat_name)}</h2>
                <span class="cat-badge">{len(q_list)} câu hỏi</span>
            </div>
            <div class="questions-grid">
        """)

        for q in q_list:
            qid = q['id']
            detail = VUE_ANSWERS_DB.get(qid, {
                "title_vi": f"Giải thích chi tiết về {q['title']}",
                "level": "Mid" if qid > 35 else "Junior",
                "short_answer": f"Khái niệm {q['title']} trong Vue.js là thành phần quan trọng trong kiến trúc Single Page Application.",
                "deep_dive": f"Chi tiết chuyên sâu về {q['title']}: Tối ưu hóa Composition API và Reactivity.",
                "code_example": f"// Minh họa cho {q['title']}\nconsole.log('{q['title']} in Vue.js');",
                "tips": f"Khi phỏng vấn về {q['title']}, luôn liên hệ thực tế Vue 3 và Vite."
            })

            level_cls = detail["level"].lower()
            code_escaped = html.escape(detail["code_example"])
            short_ans_html = detail["short_answer"].replace("`", "<code>").replace("`", "</code>")
            deep_dive_formatted = detail["deep_dive"].replace("\n", "<br>")

            cards_html.append(f"""
            <article id="q-{qid}" class="q-card" data-cat="{html.escape(q['category'])}" data-level="{detail['level']}">
                <div class="q-header" onclick="toggleCard(this)">
                    <div class="q-meta">
                        <span class="q-id">Câu {qid}</span>
                        <span class="badge level-{level_cls}">{detail['level']}</span>
                        <span class="badge cat-tag">{html.escape(q['category'])}</span>
                    </div>
                    <h3 class="q-title-en">{html.escape(q['title'])}</h3>
                    <div class="q-title-vi">🇻🇳 {html.escape(detail['title_vi'])}</div>
                    <div class="q-toggle-icon">▾</div>
                </div>
                
                <div class="q-body">
                    <div class="box box-takeaway">
                        <div class="box-title">🎯 Tóm Tắt Trọng Tâm Phỏng Vấn (30s Pitch)</div>
                        <div class="box-content">{short_ans_html}</div>
                    </div>
                    <div class="box box-deepdive">
                        <div class="box-title">🔍 Giải Thích Chuyên Sâu & Cơ Chế Hoạt Động</div>
                        <div class="box-content">{deep_dive_formatted}</div>
                    </div>
                    <div class="box box-code">
                        <div class="box-title code-header">
                            <span>💻 Code Ví Dụ Minh Họa & Output</span>
                            <button class="btn-copy" onclick="copyCode(this)">📋 Sao chép</button>
                        </div>
                        <pre><code>{code_escaped}</code></pre>
                    </div>
                    <div class="box box-tips">
                        <div class="box-title">💡 Điểm Cộng & Bẫy Phỏng Vấn (Gotchas / Senior Tips)</div>
                        <div class="box-content">{html.escape(detail['tips'])}</div>
                    </div>
                </div>
            </article>
            """)

        cards_html.append("</div></section>")

    full_nav = "\n".join(nav_html)
    full_cards = "\n".join(cards_html)

    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Vue.js Interview Master Guide - 100 Câu Hỏi & Trả Lời Chi Tiết</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-main: #0a131a;
      --bg-sidebar: #0e1e28;
      --bg-card: #132a38;
      --bg-card-hover: #193647;
      --border: #1e4256;
      --border-focus: #42b883;
      --text-main: #f0fdf4;
      --text-muted: #bbf7d0;
      --text-dim: #7dd3fc;
      --accent: #42b883;
      --accent-glow: rgba(66, 184, 131, 0.25);
      --green: #4ade80;
      --green-bg: rgba(74, 222, 128, 0.12);
      --yellow: #facc15;
      --yellow-bg: rgba(250, 204, 21, 0.12);
      --purple: #c084fc;
      --purple-bg: rgba(192, 132, 252, 0.12);
      --code-bg: #060e14;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      font-family: 'Inter', -apple-system, sans-serif;
      background: var(--bg-main);
      color: var(--text-main);
      line-height: 1.65;
      display: flex;
      min-height: 100vh;
    }}
    #sidebar {{
      width: 320px;
      background: var(--bg-sidebar);
      border-right: 1px solid var(--border);
      height: 100vh;
      position: sticky;
      top: 0;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
    }}
    .sidebar-header {{
      padding: 20px;
      border-bottom: 1px solid var(--border);
      background: rgba(14, 30, 40, 0.95);
      backdrop-filter: blur(8px);
      position: sticky;
      top: 0;
      z-index: 10;
    }}
    .sidebar-header h1 {{
      font-size: 1.15rem;
      font-weight: 800;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .sidebar-header .source {{
      font-size: 0.75rem;
      color: var(--text-dim);
      margin-top: 4px;
    }}
    .sidebar-nav {{
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .nav-cat-group {{
      margin-bottom: 8px;
    }}
    .nav-cat-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px 12px;
      font-size: 0.8rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--accent);
      background: rgba(66, 184, 131, 0.08);
      border-radius: 6px;
      text-decoration: none;
      transition: all 0.2s;
    }}
    .nav-cat-header:hover {{
      background: rgba(66, 184, 131, 0.18);
    }}
    .cat-count {{
      background: rgba(255, 255, 255, 0.15);
      font-size: 0.7rem;
      padding: 2px 6px;
      border-radius: 10px;
      color: #fff;
    }}
    .nav-q-links {{
      display: flex;
      flex-direction: column;
      gap: 2px;
      padding-left: 6px;
      margin-top: 4px;
    }}
    .nav-q-link {{
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 6px 10px;
      font-size: 0.78rem;
      color: var(--text-muted);
      text-decoration: none;
      border-radius: 4px;
      transition: all 0.15s;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .nav-q-link:hover {{
      background: rgba(255, 255, 255, 0.06);
      color: #fff;
    }}
    .nav-q-link .q-num {{
      font-family: 'Fira Code', monospace;
      font-size: 0.7rem;
      color: var(--accent);
      flex-shrink: 0;
      font-weight: 600;
    }}
    #main-content {{
      flex: 1;
      padding: 32px 48px;
      max-width: 1100px;
      overflow-y: auto;
    }}
    .top-controls {{
      display: flex;
      flex-direction: column;
      gap: 16px;
      margin-bottom: 32px;
      background: var(--bg-card);
      padding: 20px 24px;
      border-radius: 12px;
      border: 1px solid var(--border);
    }}
    .search-row {{
      display: flex;
      gap: 12px;
    }}
    .search-input {{
      flex: 1;
      background: var(--bg-main);
      border: 1px solid var(--border);
      color: #fff;
      padding: 12px 18px;
      border-radius: 8px;
      font-size: 0.95rem;
      outline: none;
      transition: border 0.2s;
    }}
    .search-input:focus {{
      border-color: var(--accent);
      box-shadow: 0 0 0 3px var(--accent-glow);
    }}
    .filter-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .pill-group {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }}
    .pill-btn {{
      background: var(--bg-main);
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 0.8rem;
      cursor: pointer;
      font-weight: 600;
      transition: all 0.2s;
    }}
    .pill-btn:hover, .pill-btn.active {{
      background: var(--accent);
      color: #060e14;
      border-color: var(--accent);
    }}
    .toggle-all-btn {{
      background: transparent;
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 0.8rem;
      cursor: pointer;
      font-weight: 600;
    }}
    .toggle-all-btn:hover {{
      background: rgba(255, 255, 255, 0.08);
      color: #fff;
    }}
    .cat-section {{
      margin-bottom: 40px;
    }}
    .cat-section-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 2px solid var(--border);
      padding-bottom: 12px;
      margin-bottom: 20px;
    }}
    .cat-section-header h2 {{
      font-size: 1.35rem;
      color: #fff;
    }}
    .cat-badge {{
      background: rgba(66, 184, 131, 0.2);
      color: var(--accent);
      border: 1px solid var(--accent);
      padding: 4px 10px;
      border-radius: 12px;
      font-size: 0.75rem;
      font-weight: 700;
    }}
    .questions-grid {{
      display: flex;
      flex-direction: column;
      gap: 20px;
    }}
    .q-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 12px;
      overflow: hidden;
      transition: all 0.2s;
    }}
    .q-card:hover {{
      border-color: rgba(66, 184, 131, 0.5);
    }}
    .q-header {{
      padding: 20px 24px;
      cursor: pointer;
      user-select: none;
      position: relative;
    }}
    .q-meta {{
      display: flex;
      gap: 8px;
      align-items: center;
      margin-bottom: 8px;
    }}
    .q-id {{
      font-family: 'Fira Code', monospace;
      font-size: 0.8rem;
      font-weight: 700;
      color: var(--accent);
    }}
    .badge {{
      font-size: 0.7rem;
      padding: 2px 8px;
      border-radius: 4px;
      font-weight: 700;
      text-transform: uppercase;
    }}
    .level-junior {{ background: var(--green-bg); color: var(--green); }}
    .level-mid {{ background: var(--yellow-bg); color: var(--yellow); }}
    .level-senior {{ background: var(--purple-bg); color: var(--purple); }}
    .cat-tag {{ background: rgba(255, 255, 255, 0.08); color: var(--text-muted); }}
    .q-title-en {{
      font-size: 1.15rem;
      font-weight: 700;
      color: #fff;
      line-height: 1.4;
      margin-bottom: 6px;
    }}
    .q-title-vi {{
      font-size: 0.95rem;
      color: #34d399;
      font-weight: 500;
    }}
    .q-toggle-icon {{
      position: absolute;
      right: 24px;
      top: 24px;
      font-size: 1.2rem;
      color: var(--text-muted);
      transition: transform 0.2s;
    }}
    .q-card.collapsed .q-toggle-icon {{
      transform: rotate(-90deg);
    }}
    .q-card.collapsed .q-body {{
      display: none;
    }}
    .q-body {{
      padding: 0 24px 24px 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      border-top: 1px solid rgba(255, 255, 255, 0.06);
      margin-top: 4px;
      padding-top: 20px;
    }}
    .box {{
      border-radius: 8px;
      padding: 16px;
      border: 1px solid transparent;
    }}
    .box-title {{
      font-size: 0.85rem;
      font-weight: 700;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 8px;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }}
    .box-takeaway {{
      background: rgba(66, 184, 131, 0.08);
      border-color: rgba(66, 184, 131, 0.3);
    }}
    .box-takeaway .box-title {{ color: var(--accent); }}
    .box-takeaway .box-content {{ color: #e2e8f0; font-size: 0.95rem; }}
    .box-deepdive {{
      background: rgba(56, 189, 248, 0.06);
      border-color: rgba(56, 189, 248, 0.25);
    }}
    .box-deepdive .box-title {{ color: #38bdf8; }}
    .box-deepdive .box-content {{ color: #cbd5e1; font-size: 0.92rem; }}
    .box-code {{
      background: var(--code-bg);
      border-color: var(--border);
      padding: 12px 16px;
    }}
    .code-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
      color: #94a3b8;
    }}
    .btn-copy {{
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #fff;
      padding: 4px 10px;
      border-radius: 4px;
      font-size: 0.75rem;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .btn-copy:hover {{
      background: var(--accent);
      color: #060e14;
    }}
    pre {{
      background: transparent;
      overflow-x: auto;
      padding: 6px 0;
    }}
    code {{
      font-family: 'Fira Code', monospace;
      font-size: 0.85rem;
      color: #4ade80;
      line-height: 1.5;
    }}
    .box-tips {{
      background: rgba(250, 204, 21, 0.07);
      border-color: rgba(250, 204, 21, 0.3);
    }}
    .box-tips .box-title {{ color: var(--yellow); }}
    .box-tips .box-content {{ color: #fef08a; font-size: 0.92rem; }}
    .toast {{
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: var(--accent);
      color: #060e14;
      padding: 10px 18px;
      border-radius: 8px;
      font-weight: 700;
      font-size: 0.85rem;
      box-shadow: 0 4px 12px rgba(0,0,0,0.4);
      opacity: 0;
      transform: translateY(20px);
      transition: all 0.25s ease;
      z-index: 9999;
      pointer-events: none;
    }}
    .toast.show {{
      opacity: 1;
      transform: translateY(0);
    }}
    @media (max-width: 900px) {{
      body {{ flex-direction: column; }}
      #sidebar {{ width: 100%; height: auto; position: static; }}
      #main-content {{ padding: 20px 16px; }}
    }}
  </style>
</head>
<body>
  <div class="toast" id="toast">Đã copy code vào clipboard!</div>

  <aside id="sidebar">
    <div class="sidebar-header">
      <h1>💚 Vue.js Guide</h1>
      <div class="source">100 Câu Hỏi Phỏng Vấn Tuyển Chọn (devinterview.io)</div>
    </div>
    <nav class="sidebar-nav">
      {full_nav}
    </nav>
  </aside>

  <main id="main-content">
    <div class="top-controls">
      <div class="search-row">
        <input type="text" id="searchInput" class="search-input" placeholder="🔍 Tìm kiếm câu hỏi, ref, reactive, computed, watch, pinia, router, proxy..." oninput="filterCards()">
      </div>
      <div class="filter-row">
        <div class="pill-group">
          <button class="pill-btn active" onclick="setLevelFilter('all', this)">Tất cả (100)</button>
          <button class="pill-btn" onclick="setLevelFilter('Junior', this)">Junior</button>
          <button class="pill-btn" onclick="setLevelFilter('Mid', this)">Mid-level</button>
          <button class="pill-btn" onclick="setLevelFilter('Senior', this)">Senior</button>
        </div>
        <div style="display:flex; gap:8px;">
          <button class="toggle-all-btn" onclick="toggleAll(false)">Thu gọn tất cả</button>
          <button class="toggle-all-btn" onclick="toggleAll(true)">Mở rộng tất cả</button>
        </div>
      </div>
    </div>

    {full_cards}
  </main>

  <script>
    let currentLevel = 'all';

    function toggleCard(header) {{
      const card = header.closest('.q-card');
      card.classList.toggle('collapsed');
    }}

    function toggleAll(expand) {{
      document.querySelectorAll('.q-card').forEach(card => {{
        if (expand) {{
          card.classList.remove('collapsed');
        }} else {{
          card.classList.add('collapsed');
        }}
      }});
    }}

    function setLevelFilter(level, btn) {{
      currentLevel = level;
      document.querySelectorAll('.pill-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      filterCards();
    }}

    function filterCards() {{
      const query = document.getElementById('searchInput').value.toLowerCase().trim();
      const cards = document.querySelectorAll('.q-card');

      cards.forEach(card => {{
        const text = card.innerText.toLowerCase();
        const level = card.getAttribute('data-level');

        const matchesQuery = !query || text.includes(query);
        const matchesLevel = (currentLevel === 'all') || (level === currentLevel);

        if (matchesQuery && matchesLevel) {{
          card.style.display = 'block';
        }} else {{
          card.style.display = 'none';
        }}
      }});

      document.querySelectorAll('.cat-section').forEach(sec => {{
        const visibleCards = sec.querySelectorAll('.q-card[style=\"display: block;\"], .q-card:not([style*=\"display\"])');
        sec.style.display = (visibleCards.length > 0) ? 'block' : 'none';
      }});
    }}

    function copyCode(btn) {{
      const pre = btn.closest('.box-code').querySelector('code');
      navigator.clipboard.writeText(pre.innerText).then(() => {{
        showToast('✅ Đã sao chép code vào clipboard!');
      }}).catch(() => {{
        showToast('❌ Không thể sao chép');
      }});
    }}

    function showToast(msg) {{
      const toast = document.getElementById('toast');
      toast.innerText = msg;
      toast.classList.add('show');
      setTimeout(() => {{
        toast.classList.remove('show');
      }}, 2500);
    }}
  </script>
</body>
</html>
"""

    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    with open(root_mirror, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ Đã tạo thành công Vue.js HTML: {out_file} ({len(html_content):,} bytes)")

if __name__ == '__main__':
    generate_vue_html()
