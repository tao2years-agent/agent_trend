from __future__ import annotations

from pathlib import Path
import html
import re

import markdown
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "outputs" / "ai-agent-collaboration-report.md"
TARGET = ROOT / "outputs" / "index.html"


def slugify(value: str) -> str:
    value = re.sub(r"\s+", "-", value.strip().lower())
    value = re.sub(r"[^\w\-\u4e00-\u9fff]", "", value)
    return value[:80] or "section"


def main() -> None:
    md = SOURCE.read_text(encoding="utf-8")
    rendered = markdown.markdown(md, extensions=["tables", "fenced_code", "toc"])
    soup = BeautifulSoup(rendered, "html.parser")
    title = soup.find("h1")
    if title:
        title.extract()
    used: set[str] = set()
    nav_items = []
    for heading in soup.find_all(["h2", "h3"]):
        base = slugify(heading.get_text(" ", strip=True))
        anchor = base
        index = 2
        while anchor in used:
            anchor = f"{base}-{index}"
            index += 1
        used.add(anchor)
        heading["id"] = anchor
        nav_items.append((heading.name, anchor, heading.get_text(" ", strip=True)))

    nav = "\n".join(
        f'<a class="nav-link {"sub" if level == "h3" else ""}" href="#{anchor}" data-label="{html.escape(label.lower())}">{html.escape(label)}</a>'
        for level, anchor, label in nav_items
    )
    body = str(soup)
    template = f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Agent 办公与组织协作深度研究</title>
  <style>
    :root {{ --bg:#f3f0e8; --paper:#fffdf8; --ink:#202724; --muted:#65706a; --line:#d8d5ca; --accent:#176c5b; --accent2:#c65d36; --code:#ece9df; }}
    * {{ box-sizing:border-box; }}
    html {{ scroll-behavior:smooth; }}
    body {{ margin:0; color:var(--ink); background:var(--bg); font-family:Inter,"Noto Sans SC","Microsoft YaHei",system-ui,sans-serif; line-height:1.72; }}
    .masthead {{ padding:42px clamp(24px,6vw,90px) 36px; background:var(--ink); color:#fff; border-bottom:5px solid var(--accent2); }}
    .eyebrow {{ color:#9ed4c7; font-size:.78rem; letter-spacing:.18em; text-transform:uppercase; }}
    h1 {{ max-width:1000px; margin:.35rem 0 .6rem; font-family:Georgia,"Noto Serif SC",serif; font-size:clamp(2rem,5vw,4.5rem); line-height:1.08; letter-spacing:-.025em; }}
    .dek {{ max-width:820px; margin:0; color:#d6ded9; font-size:1.05rem; }}
    .layout {{ display:grid; grid-template-columns:290px minmax(0,900px); gap:44px; max-width:1280px; margin:0 auto; padding:30px 24px 80px; }}
    aside {{ position:sticky; top:18px; align-self:start; max-height:calc(100vh - 36px); overflow:auto; padding:18px; background:rgba(255,253,248,.92); border:1px solid var(--line); border-radius:14px; box-shadow:0 10px 35px rgba(32,39,36,.06); }}
    .search {{ width:100%; padding:10px 12px; border:1px solid var(--line); border-radius:9px; background:#fff; font:inherit; }}
    .search:focus {{ outline:3px solid rgba(23,108,91,.18); border-color:var(--accent); }}
    nav {{ margin-top:12px; display:flex; flex-direction:column; gap:2px; }}
    .nav-link {{ color:#34413c; text-decoration:none; padding:7px 9px; border-radius:7px; font-size:.91rem; line-height:1.35; }}
    .nav-link:hover,.nav-link:focus {{ color:var(--accent); background:#edf5f1; }}
    .nav-link.sub {{ padding-left:24px; color:var(--muted); font-size:.84rem; }}
    main {{ min-width:0; background:var(--paper); border:1px solid var(--line); padding:clamp(26px,5vw,64px); box-shadow:0 18px 55px rgba(32,39,36,.08); }}
    h2,h3 {{ scroll-margin-top:24px; font-family:Georgia,"Noto Serif SC",serif; line-height:1.3; }}
    h2 {{ margin:3rem 0 1rem; padding-top:.7rem; border-top:1px solid var(--line); font-size:1.75rem; }}
    h2:first-child {{ margin-top:0; border-top:0; }}
    h3 {{ margin:2rem 0 .75rem; color:var(--accent); font-size:1.22rem; }}
    p {{ margin:.8rem 0; }}
    a {{ color:var(--accent); text-underline-offset:3px; }}
    table {{ width:100%; border-collapse:collapse; margin:1.2rem 0 1.8rem; font-size:.91rem; display:block; overflow-x:auto; }}
    th,td {{ min-width:140px; text-align:left; vertical-align:top; padding:10px 12px; border-bottom:1px solid var(--line); }}
    th {{ color:#fff; background:var(--accent); }}
    tr:nth-child(even) td {{ background:#f7f4ed; }}
    code {{ background:var(--code); padding:.12em .34em; border-radius:4px; }}
    pre {{ overflow:auto; padding:18px; background:#202724; color:#eff5f1; border-radius:10px; }}
    pre code {{ background:transparent; padding:0; }}
    blockquote {{ margin:1.4rem 0; padding:.2rem 1rem; border-left:4px solid var(--accent2); color:var(--muted); }}
    .mobile-toggle {{ display:none; }}
    .footer {{ margin-top:54px; padding-top:18px; border-top:1px solid var(--line); color:var(--muted); font-size:.85rem; }}
    @media (max-width:860px) {{
      .masthead {{ padding:30px 20px; }}
      .layout {{ display:block; padding:16px 12px 50px; }}
      aside {{ position:static; max-height:none; margin-bottom:14px; }}
      .mobile-toggle {{ display:block; width:100%; padding:10px 12px; color:#fff; background:var(--accent); border:0; border-radius:9px; font:inherit; }}
      .toc-wrap {{ display:none; }}
      aside.open .toc-wrap {{ display:block; }}
      main {{ padding:24px 18px; }}
      h1 {{ font-size:2.25rem; }}
    }}
    @media print {{ aside,.mobile-toggle {{ display:none!important; }} .layout {{ display:block; padding:0; }} main {{ border:0; box-shadow:none; }} body {{ background:#fff; }} }}
  </style>
</head>
<body>
  <header class="masthead">
    <div class="eyebrow">LLM Wiki · Product & Technical Research · 2026-11-16</div>
    <h1>AI Agent 办公软件：从单体执行到组织与跨组织协作</h1>
    <p class="dek">以 WorkBuddy、千问办公、ChatGPT Work/Codex、Claude/Claude Code 为核心，拆解团队协作产品对象、身份授权、跨组织信任与技术架构。</p>
  </header>
  <div class="layout">
    <aside id="toc-panel">
      <button class="mobile-toggle" id="toc-toggle" aria-expanded="false">展开目录</button>
      <div class="toc-wrap">
        <input class="search" id="nav-search" type="search" placeholder="筛选目录…" aria-label="筛选目录">
        <nav aria-label="文章目录">{nav}</nav>
      </div>
    </aside>
    <main id="report">{body}<div class="footer">离线研究视图。详细来源、覆盖和未决问题见同目录知识库。</div></main>
  </div>
  <script>
    const panel=document.getElementById('toc-panel');
    const toggle=document.getElementById('toc-toggle');
    toggle.addEventListener('click',()=>{{
      const open=panel.classList.toggle('open');
      toggle.setAttribute('aria-expanded',String(open));
      toggle.textContent=open?'收起目录':'展开目录';
    }});
    const search=document.getElementById('nav-search');
    search.addEventListener('input',()=>{{
      const q=search.value.trim().toLowerCase();
      document.querySelectorAll('.nav-link').forEach(link=>{{link.hidden=q && !link.dataset.label.includes(q);}});
    }});
  </script>
</body>
</html>'''
    TARGET.write_text(template, encoding="utf-8")
    print(f"wrote {TARGET} ({TARGET.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
