import os
import urllib.parse
import re

# 生成index.html页面的脚本

PAGES_DIR = "pages"
OUTPUT_FILE = "index.html"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Pages Collection</title>
    <style>
        :root {{
            --bg: #ffffff;
            --fg: #000000;
            --gray: #f4f4f4;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background-color: var(--bg);
            color: var(--fg);
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            line-height: 1.6;
            padding: 40px 20px;
            max-width: 800px;
            margin: 0 auto;
        }}
        header {{
            margin-bottom: 60px;
            padding-bottom: 20px;
            border-bottom: 2px solid var(--fg);
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }}
        h1 {{ font-size: 24px; font-weight: 700; letter-spacing: -0.5px; text-transform: uppercase; }}
        .count {{ font-size: 14px; font-family: monospace; }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
        }}
        
        a.card {{
            display: block;
            text-decoration: none;
            color: var(--fg);
            border: 1px solid var(--fg);
            padding: 25px;
            transition: all 0.2s ease;
            position: relative;
            background: var(--bg);
        }}
        
        a.card:hover {{
            background: var(--fg);
            color: var(--bg);
            transform: translateY(-2px);
            box-shadow: 4px 4px 0px rgba(0,0,0,0.1);
        }}

        .card-title {{
            font-weight: 600;
            font-size: 16px;
            margin-bottom: 5px;
            display: block;
        }}
        
        .card-ext {{
            font-size: 10px;
            font-family: monospace;
            opacity: 0.6;
            text-transform: uppercase;
        }}

        footer {{
            margin-top: 60px;
            font-size: 12px;
            color: #666;
            text-align: center;
            font-family: monospace;
        }}
    </style>
</head>
<body>

    <header>
        <h1>Login Collection</h1>
        <span class="count">TOTAL: {count}</span>
    </header>

    <div class="grid">
        {links}
    </div>

    <footer>
        Last updated: {timestamp}
    </footer>

</body>
</html>
"""


def natural_sort_key(s):
    return [
        int(text) if text.isdigit() else text.lower() for text in re.split(r"(\d+)", s)
    ]


def generate_index():
    links_html = ""

    if not os.path.exists(PAGES_DIR):
        print(f" 找不到 '{PAGES_DIR}' 文件夹")
        return

    files = [f for f in os.listdir(PAGES_DIR) if f.endswith(".html")]
    files.sort(key=natural_sort_key)
    file_count = len(files)

    for filename in files:
        display_name = filename.replace(".html", "").replace("-", " ").replace("_", " ")
        safe_url = urllib.parse.quote(filename)

        links_html += f"""
        <a href="{PAGES_DIR}/{safe_url}" class="card" target="_blank">
            <span class="card-title">{display_name}</span>
            <span class="card-ext">.HTML</span>
        </a>
        """

    # 生成最终 HTML
    import datetime

    final_html = HTML_TEMPLATE.format(
        links=links_html,
        count=str(file_count).zfill(2),
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"成功! 已生成 {OUTPUT_FILE}，包含 {file_count} 个页面。")


if __name__ == "__main__":
    generate_index()
