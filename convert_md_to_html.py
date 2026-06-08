#!/usr/bin/env python3
"""Convert all .md files in the project to styled .html for GitHub Pages."""
import markdown
import os
import re
from html import escape

WORKSPACE = "/home/xmren/Documents/ebooks/karina book/F2/History CH/4ai"

CSS = """
body {
  font-family: -apple-system, "Noto Sans SC", "Microsoft YaHei", sans-serif;
  background: #f5f0eb;
  color: #2c2c2c;
  line-height: 1.9;
  font-size: 16px;
  padding: 20px;
  margin: 0;
}
.container {
  max-width: 800px;
  margin: 0 auto;
  background: #fff;
  padding: 40px 48px;
  border-radius: 12px;
  box-shadow: 0 2px 20px rgba(0,0,0,0.08);
}
h1 { font-size: 26px; color: #5a2d0c; border-bottom: 2px solid #f0e8dc; padding-bottom: 8px; }
h2 { font-size: 20px; color: #5a2d0c; margin-top: 28px; }
h3 { font-size: 17px; color: #8b4513; margin-top: 22px; }
h4 { font-size: 15px; color: #8b4513; margin-top: 16px; }
a { color: #8b4513; text-decoration: none; }
a:hover { text-decoration: underline; }
p { margin: 10px 0; }
strong { color: #333; }
blockquote {
  border-left: 4px solid #d4a574;
  margin: 14px 0;
  padding: 10px 16px;
  background: #faf5ef;
  border-radius: 4px;
  color: #555;
}
code {
  background: #f0e8dc;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 14px;
}
pre {
  background: #2c2c2c;
  color: #e0e0e0;
  padding: 14px 18px;
  border-radius: 8px;
  overflow-x: auto;
  font-size: 14px;
  line-height: 1.5;
}
pre code { background: transparent; padding: 0; color: inherit; }
table {
  border-collapse: collapse;
  width: 100%;
  margin: 14px 0;
  font-size: 14px;
}
th, td {
  border: 1px solid #e0d5c8;
  padding: 8px 12px;
  text-align: left;
}
th { background: #f5f0eb; font-weight: 600; color: #5a2d0c; }
tr:nth-child(even) { background: #faf5ef; }
ul, ol { padding-left: 24px; margin: 10px 0; }
li { margin: 4px 0; }
hr { border: none; border-top: 1px solid #e0d5c8; margin: 24px 0; }
.nav-bar {
  text-align: center; padding: 10px 0 20px;
  font-size: 14px; color: #888;
}
.nav-bar a { margin: 0 8px; }
.back-link { display: block; margin-bottom: 16px; }
.back-link a { font-size: 14px; color: #8b4513; }
@media (max-width: 600px) {
  .container { padding: 16px; }
  table { font-size: 13px; }
  th, td { padding: 4px 6px; }
}
"""

MD_FILES = [
    "技能框架_史料分析.md",
    "技能框架_因果鏈分析.md",
    "技能框架_對比分析.md",
    "技能框架_評價分析.md",
    "認知深度索引圖.md",
    "互動溫習工作紙.md",
    "三天溫習計劃.md",
    "考試範圍_集中溫習.md",
    "agent_handoff_deliverable.md",
    "from_geo/agent_handoff_history_methodology.md",
]

# Map MD paths to HTML paths (same dir, .html extension)
def md_to_html_path(md_path):
    base = os.path.splitext(md_path)[0]
    return base + ".html"

def extract_title(md_content):
    """Extract the first h1 heading as the page title."""
    m = re.search(r'^#\s+(.+?)$', md_content, re.MULTILINE)
    return m.group(1).strip() if m else "中二中國歷史"

def convert_file(md_relpath):
    md_abspath = os.path.join(WORKSPACE, md_relpath)
    if not os.path.exists(md_abspath):
        print(f"  NOT FOUND: {md_relpath}")
        return
    with open(md_abspath, "r", encoding="utf-8") as f:
        md_content = f.read()
    title = extract_title(md_content)
    html_body = markdown.markdown(md_content, extensions=["tables", "fenced_code", "codehilite"])
    # Build nav backlink
    parent_dir = os.path.dirname(md_relpath)
    if parent_dir:
        back_path = "../" if parent_dir else "./"
        back_link = f'<a href="{back_path}index.html">← 返回首頁</a>'
    else:
        back_link = '<a href="index.html">← 返回首頁</a>'
    html = f"""<!DOCTYPE html>
<html lang="zh-HK">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(title)} · 中二中國歷史</title>
<style>{CSS}</style>
</head>
<body>
<div class="container">
<div class="back-link">{back_link}</div>
{html_body}
<div class="nav-bar">
<a href="index.html">🏠 返回首頁</a>
</div>
</div>
</body>
</html>"""
    html_path = os.path.join(WORKSPACE, md_to_html_path(md_relpath))
    os.makedirs(os.path.dirname(html_path), exist_ok=True)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  OK: {md_relpath} → {os.path.relpath(html_path, WORKSPACE)}")

if __name__ == "__main__":
    print(f"Converting {len(MD_FILES)} markdown files...")
    for f in MD_FILES:
        convert_file(f)
    print("Done.")
