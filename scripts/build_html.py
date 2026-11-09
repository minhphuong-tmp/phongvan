# -*- coding: utf-8 -*-
import sys
import html
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from part1 import DATA_PART_1
from part2 import DATA_PART_2
from part3 import DATA_PART_3
from part4 import DATA_PART_4

ALL_QUESTIONS = DATA_PART_1 + DATA_PART_2 + DATA_PART_3 + DATA_PART_4
ALL_QUESTIONS.sort(key=lambda x: x["id"])

# Group by category
CATEGORIES = {}
for q in ALL_QUESTIONS:
    cat = q["category"]
    if cat not in CATEGORIES:
        CATEGORIES[cat] = []
    CATEGORIES[cat].append(q)

def render_html():
    category_nav_html = []
    for cat_name, q_list in CATEGORIES.items():
        cat_id = cat_name.lower().replace(" ", "-").replace("&", "and")
        category_nav_html.append(f"""
        <div class="nav-cat-group">
            <a href="#{cat_id}" class="nav-cat-header">
                <span>{html.escape(cat_name)}</span>
                <span class="cat-count">{len(q_list)}</span>
            </a>
            <div class="nav-q-links">
        """)
        for q in q_list:
            category_nav_html.append(f"""
                <a href="#q-{q['id']}" class="nav-q-link" title="{html.escape(q['title_en'])}">
                    <span class="q-num">Q{q['id']}</span>
                    <span class="q-sub">{html.escape(q['title_en'][:40])}...</span>
                </a>
            """)
        category_nav_html.append("</div></div>")

    cards_html = []
    for cat_name, q_list in CATEGORIES.items():
        cat_id = cat_name.lower().replace(" ", "-").replace("&", "and")
        cards_html.append(f"""
        <section id="{cat_id}" class="cat-section">
            <div class="cat-section-header">
                <h2>📁 {html.escape(cat_name)}</h2>
                <span class="cat-badge">{len(q_list)} câu hỏi</span>
            </div>
            <div class="questions-grid">
        """)
        for q in q_list:
            level_cls = q["level"].lower()
            code_escaped = html.escape(q["code_example"])
            short_ans_html = q["short_answer"].replace("`", "<code>").replace("`", "</code>")
            
            # Format deep dive lines
            deep_dive_formatted = q["deep_dive"].replace("\n", "<br>")

            cards_html.append(f"""
            <article id="q-{q['id']}" class="q-card" data-cat="{html.escape(q['category'])}" data-level="{q['level']}">
                <div class="q-header" onclick="toggleCard(this)">
                    <div class="q-meta">
                        <span class="q-id">Câu {q['id']}</span>
                        <span class="badge level-{level_cls}">{q['level']}</span>
                        <span class="badge cat-tag">{html.escape(q['category'])}</span>
                    </div>
                    <h3 class="q-title-en">{html.escape(q['title_en'])}</h3>
                    <div class="q-title-vi">🇻🇳 {html.escape(q['title_vi'])}</div>
                    <div class="q-toggle-icon">▾</div>
                </div>
                
                <div class="q-body">
                    <!-- Key Takeaway -->
                    <div class="box box-takeaway">
                        <div class="box-title">🎯 Tóm Tắt Trọng Tâm Phỏng Vấn (30s Pitch)</div>
                        <div class="box-content">{short_ans_html}</div>
                    </div>

                    <!-- Deep Dive -->
                    <div class="box box-deepdive">
                        <div class="box-title">🔍 Giải Thích Chuyên Sâu & Cơ Chế Hoạt Động</div>
                        <div class="box-content">{deep_dive_formatted}</div>
                    </div>

                    <!-- Code Example -->
                    <div class="box box-code">
                        <div class="box-title code-header">
                            <span>💻 Code Ví Dụ Minh Họa & Output</span>
                            <button class="btn-copy" onclick="copyCode(this)">📋 Sao chép</button>
                        </div>
                        <pre><code>{code_escaped}</code></pre>
                    </div>

                    <!-- Gotchas & Tips -->
                    <div class="box box-tips">
                        <div class="box-title">💡 Điểm Cộng & Bẫy Phỏng Vấn (Gotchas / Senior Tips)</div>
                        <div class="box-content">{html.escape(q['tips'])}</div>
                    </div>
                </div>
            </article>
            """)
        cards_html.append("</div></section>")

    cat_options_html = ['<option value="ALL">Tất cả danh mục (13 danh mục)</option>']
    for cat_name in CATEGORIES.keys():
        cat_options_html.append(f'<option value="{html.escape(cat_name)}">{html.escape(cat_name)} ({len(CATEGORIES[cat_name])})</option>')

    full_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>100 Câu Hỏi Phỏng Vấn Python Chuyên Sâu 2026 - Giải Chi Tiết Kèm Code Ví Dụ (Devinterview.io)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-main: #0b1120;
      --bg-sidebar: #0f172a;
      --bg-card: #1e293b;
      --bg-card-hover: #243248;
      --bg-box: #0f172a;
      --border: #334155;
      --border-focus: #38bdf8;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --accent: #38bdf8;
      --accent-glow: rgba(56, 189, 248, 0.15);
      --green: #4ade80;
      --green-bg: rgba(74, 222, 128, 0.08);
      --yellow: #facc15;
      --yellow-bg: rgba(250, 204, 21, 0.08);
      --purple: #c084fc;
      --purple-bg: rgba(192, 132, 252, 0.08);
      --orange: #fb923c;
      --code-bg: #030712;
    }}
    
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: var(--bg-main);
      color: var(--text-main);
      line-height: 1.65;
      display: flex;
      min-height: 100vh;
    }}

    /* SIDEBAR NAVIGATION */
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
      z-index: 40;
    }}
    .sidebar-header {{
      padding: 20px;
      border-bottom: 1px solid var(--border);
      background: #090e1a;
    }}
    .sidebar-header h1 {{
      font-size: 1.15rem;
      font-weight: 800;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .sidebar-header .source {{
      font-size: 0.78rem;
      color: var(--accent);
      margin-top: 4px;
    }}
    .sidebar-nav {{
      padding: 12px 10px 40px;
      flex: 1;
    }}
    .nav-cat-group {{
      margin-bottom: 14px;
    }}
    .nav-cat-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--text-muted);
      text-decoration: none;
      padding: 8px 10px;
      border-radius: 6px;
      transition: all 0.15s;
    }}
    .nav-cat-header:hover {{
      color: var(--accent);
      background: rgba(56, 189, 248, 0.08);
    }}
    .cat-count {{
      background: #1e293b;
      padding: 2px 7px;
      border-radius: 10px;
      font-size: 0.72rem;
      color: var(--text-dim);
    }}
    .nav-q-links {{
      display: flex;
      flex-direction: column;
      padding-left: 8px;
      margin-top: 4px;
      gap: 2px;
    }}
    .nav-q-link {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.75rem;
      color: #64748b;
      text-decoration: none;
      padding: 4px 8px;
      border-radius: 4px;
      transition: all 0.15s;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .nav-q-link:hover {{
      color: #f1f5f9;
      background: #1e293b;
    }}
    .nav-q-link .q-num {{
      font-family: 'Fira Code', monospace;
      color: var(--accent);
      font-weight: 600;
      font-size: 0.7rem;
    }}

    /* MAIN CONTAINER */
    #main-content {{
      flex: 1;
      min-width: 0;
      padding: 24px 32px 120px;
      max-width: 1200px;
      margin: 0 auto;
    }}

    /* TOP STICKY TOOLBAR */
    .toolbar {{
      position: sticky;
      top: 16px;
      z-index: 30;
      background: rgba(11, 17, 32, 0.92);
      backdrop-filter: blur(12px);
      padding: 14px 18px;
      border-radius: 14px;
      border: 1px solid var(--border);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
      margin-bottom: 30px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .toolbar-row-1 {{
      display: flex;
      gap: 12px;
      align-items: center;
      flex-wrap: wrap;
    }}
    .search-box {{
      flex: 1;
      min-width: 260px;
      position: relative;
    }}
    .search-input {{
      width: 100%;
      background: #0f172a;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 10px 14px 10px 38px;
      color: #fff;
      font-size: 0.9rem;
      outline: none;
      transition: border 0.2s;
    }}
    .search-input:focus {{
      border-color: var(--border-focus);
      box-shadow: 0 0 0 3px var(--accent-glow);
    }}
    .search-icon {{
      position: absolute;
      left: 12px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-dim);
    }}
    .select-filter {{
      background: #0f172a;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 10px 14px;
      color: #f1f5f9;
      font-size: 0.85rem;
      outline: none;
      cursor: pointer;
    }}
    .toolbar-row-2 {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
      font-size: 0.82rem;
    }}
    .btn-group {{
      display: flex;
      gap: 8px;
    }}
    .btn {{
      background: #1e293b;
      border: 1px solid var(--border);
      color: #cbd5e1;
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 0.8rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s;
    }}
    .btn:hover {{
      background: var(--accent);
      color: #0b1120;
    }}
    .count-indicator {{
      color: var(--text-muted);
      font-weight: 500;
    }}
    .count-indicator strong {{
      color: var(--accent);
    }}

    /* HERO BANNER */
    .hero {{
      margin-bottom: 30px;
      padding: 24px;
      background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
      border: 1px solid var(--border);
      border-radius: 16px;
      position: relative;
      overflow: hidden;
    }}
    .hero h1 {{
      font-size: 1.85rem;
      font-weight: 800;
      color: #fff;
      margin-bottom: 8px;
    }}
    .hero p {{
      color: var(--text-muted);
      font-size: 0.95rem;
      max-width: 800px;
    }}

    /* CATEGORY SECTION */
    .cat-section {{
      margin-bottom: 40px;
    }}
    .cat-section-header {{
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 18px;
      padding-bottom: 10px;
      border-bottom: 2px solid var(--border);
    }}
    .cat-section-header h2 {{
      font-size: 1.35rem;
      font-weight: 700;
      color: var(--accent);
    }}
    .cat-badge {{
      background: #1e293b;
      color: var(--text-muted);
      font-size: 0.78rem;
      padding: 4px 10px;
      border-radius: 12px;
      font-weight: 600;
      border: 1px solid var(--border);
    }}

    /* QUESTION CARDS */
    .questions-grid {{
      display: flex;
      flex-direction: column;
      gap: 18px;
    }}
    .q-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 14px;
      overflow: hidden;
      transition: all 0.2s ease;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    }}
    .q-card:hover {{
      border-color: #475569;
    }}
    .q-header {{
      padding: 18px 22px;
      cursor: pointer;
      position: relative;
      user-select: none;
      background: #1a2436;
      border-bottom: 1px solid transparent;
      transition: background 0.15s;
    }}
    .q-card.opened .q-header {{
      border-bottom-color: var(--border);
      background: #151d2c;
    }}
    .q-meta {{
      display: flex;
      gap: 8px;
      align-items: center;
      margin-bottom: 8px;
      flex-wrap: wrap;
    }}
    .q-id {{
      font-family: 'Fira Code', monospace;
      font-size: 0.8rem;
      font-weight: 700;
      color: var(--accent);
      background: rgba(56, 189, 248, 0.12);
      padding: 2px 8px;
      border-radius: 6px;
    }}
    .badge {{
      font-size: 0.72rem;
      font-weight: 600;
      padding: 2px 8px;
      border-radius: 6px;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }}
    .level-junior {{ background: var(--green-bg); color: var(--green); border: 1px solid rgba(74, 222, 128, 0.3); }}
    .level-mid {{ background: var(--yellow-bg); color: var(--yellow); border: 1px solid rgba(250, 204, 21, 0.3); }}
    .level-senior {{ background: var(--purple-bg); color: var(--purple); border: 1px solid rgba(192, 132, 252, 0.3); }}
    .cat-tag {{ background: #0f172a; color: var(--text-dim); border: 1px solid var(--border); }}

    .q-title-en {{
      font-size: 1.12rem;
      font-weight: 700;
      color: #fff;
      line-height: 1.4;
      margin-bottom: 6px;
      padding-right: 30px;
    }}
    .q-title-vi {{
      font-size: 0.92rem;
      color: #94a3b8;
      font-weight: 500;
    }}
    .q-toggle-icon {{
      position: absolute;
      right: 20px;
      top: 24px;
      font-size: 1.4rem;
      color: var(--text-dim);
      transition: transform 0.25s ease;
    }}
    .q-card.opened .q-toggle-icon {{
      transform: rotate(180deg);
      color: var(--accent);
    }}

    /* QUESTION BODY (COLLAPSIBLE) */
    .q-body {{
      display: none;
      padding: 22px;
      background: var(--bg-card);
      flex-direction: column;
      gap: 16px;
    }}
    .q-card.opened .q-body {{
      display: flex;
    }}

    /* BOXES */
    .box {{
      border-radius: 10px;
      padding: 16px 18px;
      font-size: 0.92rem;
    }}
    .box-title {{
      font-weight: 700;
      font-size: 0.88rem;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .box-content {{
      color: #cbd5e1;
      line-height: 1.68;
    }}
    .box-content code {{
      font-family: 'Fira Code', monospace;
      font-size: 0.83rem;
      background: #030712;
      color: #38bdf8;
      padding: 2px 6px;
      border-radius: 4px;
      border: 1px solid #1e293b;
    }}
    .box-content table {{
      width: 100%;
      border-collapse: collapse;
      margin: 12px 0;
      font-size: 0.85rem;
    }}
    .box-content th, .box-content td {{
      border: 1px solid var(--border);
      padding: 8px 12px;
      text-align: left;
    }}
    .box-content th {{
      background: #0f172a;
      color: var(--accent);
    }}

    .box-takeaway {{
      background: rgba(56, 189, 248, 0.05);
      border-left: 4px solid var(--accent);
    }}
    .box-takeaway .box-title {{ color: var(--accent); }}

    .box-deepdive {{
      background: #0f172a;
      border-left: 4px solid var(--purple);
      border: 1px solid #1e293b;
      border-left-width: 4px;
    }}
    .box-deepdive .box-title {{ color: var(--purple); }}

    .box-code {{
      background: var(--code-bg);
      border: 1px solid #1e293b;
      border-radius: 10px;
      padding: 0;
      overflow: hidden;
    }}
    .code-header {{
      background: #0d131f;
      padding: 10px 16px;
      border-bottom: 1px solid #1e293b;
      display: flex;
      justify-content: space-between;
      align-items: center;
      color: #94a3b8;
      font-size: 0.8rem;
      margin-bottom: 0;
    }}
    .btn-copy {{
      background: #1e293b;
      border: 1px solid #334155;
      color: #cbd5e1;
      padding: 4px 10px;
      border-radius: 5px;
      font-size: 0.75rem;
      cursor: pointer;
      transition: all 0.15s;
    }}
    .btn-copy:hover {{
      background: var(--accent);
      color: #0b1120;
    }}
    .box-code pre {{
      padding: 16px;
      overflow-x: auto;
      font-family: 'Fira Code', monospace;
      font-size: 0.85rem;
      color: #e2e8f0;
      line-height: 1.55;
    }}

    .box-tips {{
      background: rgba(250, 204, 21, 0.05);
      border-left: 4px solid var(--yellow);
    }}
    .box-tips .box-title {{ color: var(--yellow); }}

    /* BACK TO TOP */
    #back-to-top {{
      position: fixed;
      bottom: 24px;
      right: 28px;
      background: var(--accent);
      color: #0b1120;
      width: 42px;
      height: 42px;
      border-radius: 50%;
      border: none;
      font-size: 1.2rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 16px rgba(56, 189, 248, 0.4);
      opacity: 0;
      pointer-events: none;
      transition: all 0.25s ease;
      z-index: 50;
    }}
    #back-to-top.visible {{
      opacity: 1;
      pointer-events: auto;
    }}

    /* RESPONSIVE */
    @media (max-width: 900px) {{
      #sidebar {{ display: none; }}
      #main-content {{ padding: 16px 12px 100px; }}
      .hero h1 {{ font-size: 1.45rem; }}
    }}
  </style>
</head>
<body>

  <!-- LEFT SIDEBAR -->
  <aside id="sidebar">
    <div class="sidebar-header">
      <h1>🐍 Python 100 Q&A</h1>
      <div class="source">Devinterview.io Master Guide 2026</div>
    </div>
    <nav class="sidebar-nav">
      {''.join(category_nav_html)}
    </nav>
  </aside>

  <!-- MAIN CONTENT -->
  <main id="main-content">
    
    <div class="hero">
      <h1>100 Câu Hỏi Phỏng Vấn Python Cốt Lõi 2026</h1>
      <p>Cẩm nang giải chi tiết 100 câu hỏi phỏng vấn chuẩn mực từ Devinterview.io. Được biên soạn đầy đủ với 4 khối thông tin: Tóm tắt 30s phỏng vấn, Cơ chế CPython chuyên sâu (Under the hood), Code thực chiến chuẩn PEP 8 và Điểm cộng/Bẫy phỏng vấn (Gotchas & Senior Tips).</p>
    </div>

    <!-- STICKY TOOLBAR -->
    <div class="toolbar">
      <div class="toolbar-row-1">
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input type="text" id="searchInput" class="search-input" placeholder="Tìm kiếm câu hỏi (vd: GIL, decorator, mutable, generator, pandas, yield...)" oninput="handleSearch()">
        </div>
        <select id="catFilter" class="select-filter" onchange="handleFilter()">
          {''.join(cat_options_html)}
        </select>
        <select id="levelFilter" class="select-filter" onchange="handleFilter()">
          <option value="ALL">Tất cả cấp độ</option>
          <option value="Junior">Junior</option>
          <option value="Mid">Mid-Level</option>
          <option value="Senior">Senior</option>
        </select>
      </div>
      <div class="toolbar-row-2">
        <div class="btn-group">
          <button class="btn" onclick="expandAll(true)">📂 Mở tất cả (Expand All)</button>
          <button class="btn" onclick="expandAll(false)">📁 Thu gọn (Collapse All)</button>
        </div>
        <div class="count-indicator">
          Đang hiển thị: <strong id="visibleCount">100</strong> / 100 câu hỏi
        </div>
      </div>
    </div>

    <!-- QUESTIONS CONTENT -->
    <div id="questionsContainer">
      {''.join(cards_html)}
    </div>

  </main>

  <button id="back-to-top" onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})" title="Lên đầu trang">▲</button>

  <script>
    // Toggle Single Card
    function toggleCard(headerEl) {{
      const card = headerEl.closest('.q-card');
      card.classList.toggle('opened');
    }}

    // Expand / Collapse All
    function expandAll(isOpen) {{
      document.querySelectorAll('.q-card').forEach(card => {{
        if (card.style.display !== 'none') {{
          if (isOpen) {{
            card.classList.add('opened');
          }} else {{
            card.classList.remove('opened');
          }}
        }}
      }});
    }}

    // Copy Code to Clipboard
    function copyCode(btn) {{
      const pre = btn.closest('.box-code').querySelector('pre code');
      navigator.clipboard.writeText(pre.innerText).then(() => {{
        const originalText = btn.innerText;
        btn.innerText = ' Đã chép!';
        btn.style.background = '#4ade80';
        btn.style.color = '#0b1120';
        setTimeout(() => {{
          btn.innerText = originalText;
          btn.style.background = '';
          btn.style.color = '';
        }}, 1800);
      }});
    }}

    // Search & Filter
    function handleSearch() {{
      handleFilter();
    }}

    function handleFilter() {{
      const query = document.getElementById('searchInput').value.toLowerCase().trim();
      const catVal = document.getElementById('catFilter').value;
      const levelVal = document.getElementById('levelFilter').value;
      
      let count = 0;
      const cards = document.querySelectorAll('.q-card');

      cards.forEach(card => {{
        const cardCat = card.getAttribute('data-cat');
        const cardLevel = card.getAttribute('data-level');
        const cardText = card.innerText.toLowerCase();

        const matchQuery = !query || cardText.includes(query);
        const matchCat = (catVal === 'ALL') || (cardCat === catVal);
        const matchLevel = (levelVal === 'ALL') || (cardLevel === levelVal);

        if (matchQuery && matchCat && matchLevel) {{
          card.style.display = 'block';
          count++;
        }} else {{
          card.style.display = 'none';
        }}
      }});

      // Hide empty category sections
      document.querySelectorAll('.cat-section').forEach(sec => {{
        const visibleInSec = sec.querySelectorAll('.q-card[style="display: block;"]').length;
        const totalCardsInSec = sec.querySelectorAll('.q-card').length;
        const isHidden = (sec.querySelectorAll('.q-card[style="display: none;"]').length === totalCardsInSec);
        sec.style.display = isHidden ? 'none' : 'block';
      }});

      document.getElementById('visibleCount').innerText = count;
    }}

    // Back to top button visibility
    window.addEventListener('scroll', () => {{
      const btn = document.getElementById('back-to-top');
      if (window.scrollY > 400) {{
        btn.classList.add('visible');
      }} else {{
        btn.classList.remove('visible');
      }}
    }});

    // Auto open card if anchor linked
    window.addEventListener('load', () => {{
      if (window.location.hash) {{
        const target = document.querySelector(window.location.hash);
        if (target && target.classList.contains('q-card')) {{
          target.classList.add('opened');
          target.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
        }}
      }}
    }});
  </script>
</body>
</html>
"""
    return full_html

if __name__ == "__main__":
    html_content = render_html()
    
    out_dir_python = Path("/Users/macos/Desktop/phongvan/python")
    out_dir_phongvan = Path("/Users/macos/Desktop/phongvan")
    
    out_dir_python.mkdir(parents=True, exist_ok=True)
    
    out_file_1 = out_dir_python / "devinterview_python_100_answers.html"
    out_file_2 = out_dir_phongvan / "devinterview_python_100_answers.html"
    
    out_file_1.write_text(html_content, encoding="utf-8")
    out_file_2.write_text(html_content, encoding="utf-8")
    
    print(f"✅ Đã tạo thành công: {out_file_1} ({len(html_content):,} bytes)")
    print(f"✅ Đã sao chép sang: {out_file_2}")
