"""
build.py — wheatBread1306 Blog ビルドスクリプト

使い方:
  python build.py          # posts/ の全記事をビルド
  python build.py --help   # このメッセージを表示

生成されるファイル:
  blog/index.html          # 記事一覧ページ
  blog/<slug>/index.html   # 各記事ページ
"""

import markdown2
import os
import re
import sys

# ── 設定 ──────────────────────────────────────────────
POSTS_DIR  = "posts"        # Markdownファイルの置き場所
OUTPUT_DIR = "blog"         # 出力先
SITE_URL   = "https://wheatbread.dev"
# ────────────────────────────────────────────────────────


def parse_frontmatter(text):
    """
    ---
    key: value
    ---
    の形式のFrontmatterをパースして (metadata dict, 本文) を返す。
    """
    if not text.startswith("---"):
        return {}, text

    end = text.find("---", 3)
    if end == -1:
        return {}, text

    fm_text = text[3:end].strip()
    body    = text[end + 3:].strip()

    meta = {}
    for line in fm_text.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            meta[key.strip()] = val.strip()

    return meta, body


def build_post_html(meta, body_html, slug):
    """記事1ページ分のHTMLを返す。"""

    title       = meta.get("title",       "無題")
    title_en    = meta.get("title_en",    title)
    date        = meta.get("date",        "")
    tags_raw    = meta.get("tags",        "")
    description = meta.get("description", "")
    desc_en     = meta.get("description_en", description)

    # タグをバッジに変換
    tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
    tag_badges = "".join(
        f'<span class="blog-tag">{t}</span>' for t in tags
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title class="tl" data-ja="{title} | wheatBread1306" data-en="{title_en} | wheatBread1306">{title_en} | wheatBread1306</title>
  <meta name="description" content="{desc_en}">
  <meta property="og:title"       content="{title_en}">
  <meta property="og:description" content="{desc_en}">
  <meta property="og:url"         content="{SITE_URL}/blog/{slug}/">
  <link rel="icon" type="image/jpeg" href="../../assets/ICON.jpg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../css/style.css">
  <link rel="stylesheet" href="../../css/blog.css">
</head>
<body>

  <!-- Navigation（既存と同じ構造） -->
  <header>
    <div class="container">
      <nav>
        <a href="../../" class="logo">wheatBread1306.</a>
        <div class="nav-group">
          <div class="nav-links">
            <a href="../../#about" class="tl" data-ja="アバウト" data-en="About">About</a>
            <a href="../../#tech"  class="tl" data-ja="技術"     data-en="Tech">Tech</a>
            <a href="../../#works" class="tl" data-ja="ワークス" data-en="Works">Works</a>
            <a href="../../blog/"  class="tl" data-ja="ブログ"   data-en="Blog">Blog</a>
          </div>
          <button class="lang-toggle" onclick="toggleLanguage()" aria-label="Toggle language">
            <span id="lang-ja">JA</span><span>/</span><span id="lang-en" class="active">EN</span>
          </button>
        </div>
      </nav>
    </div>
  </header>

    <main class="blog-post-main" style="padding-top: 12rem;">
    <div class="container blog-container">

      <a href="../../blog/" class="blog-back tl" data-ja="← ブログ一覧" data-en="← Back to Blog">← Back to Blog</a>

      <article>
        <header class="post-header">
          <div class="post-meta">
            <time datetime="{date}">{date}</time>
            <div class="post-tags">{tag_badges}</div>
          </div>
          <h1 class="post-title tl" data-ja="{title}" data-en="{title_en}">{title_en}</h1>
        </header>

        <div class="post-body">
          {body_html}
        </div>
      </article>

    </div>
  </main>

  <footer>
    <div class="container">
      <p>&copy; 2026 wheatBread1306. All rights reserved.</p>
    </div>
  </footer>

  <script src="/js/script.js"></script>
</body>
</html>
"""


def build_index_html(posts):
    """
    posts: [{"slug":..., "title":..., "title_en":..., "date":..., "tags":..., "description":...}, ...]
    新しい順にソートされていることを前提とする。
    """

    cards = ""
    for p in posts:
        tags = [t.strip() for t in p["tags"].split(",") if t.strip()]
        tag_badges = "".join(f'<span class="blog-tag">{t}</span>' for t in tags)
        cards += f"""
        <a href="{p['slug']}/" class="post-card">
          <div class="post-card-meta">
            <time datetime="{p['date']}">{p['date']}</time>
            <div class="post-tags">{tag_badges}</div>
          </div>
          <h2 class="post-card-title tl" data-ja="{p['title']}" data-en="{p['title_en']}">{p['title_en']}</h2>
          <p class="post-card-desc tl" data-ja="{p['description']}" data-en="{p['description_en']}">{p['description_en']}</p>
        </a>
"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Blog | wheatBread1306</title>
  <meta name="description" content="wheatBread1306 — Audio plugin development blog.">
  <link rel="icon" type="image/jpeg" href="../assets/ICON.jpg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/style.css">
  <link rel="stylesheet" href="../css/blog.css">
</head>
<body>

  <header>
    <div class="container">
      <nav>
        <a href="../" class="logo">wheatBread1306.</a>
        <div class="nav-group">
          <div class="nav-links">
            <a href="../#about" class="tl" data-ja="アバウト" data-en="About">About</a>
            <a href="../#tech"  class="tl" data-ja="技術"     data-en="Tech">Tech</a>
            <a href="../#works" class="tl" data-ja="ワークス" data-en="Works">Works</a>
            <a href="../blog/"  class="tl" data-ja="ブログ"   data-en="Blog">Blog</a>
          </div>
          <button class="lang-toggle" onclick="toggleLanguage()" aria-label="Toggle language">
            <span id="lang-ja">JA</span><span>/</span><span id="lang-en" class="active">EN</span>
          </button>
        </div>
      </nav>
    </div>
  </header>

  <main style="padding-top: 6rem;">
    <div class="container">
      <h1 class="section-title tl" data-ja="ブログ" data-en="Blog">Blog</h1>
      <div class="post-list">
        {cards}
      </div>
    </div>
  </main>

  <footer>
    <div class="container">
      <p>&copy; 2026 wheatBread1306. All rights reserved.</p>
    </div>
  </footer>

  <script src="../js/script.js"></script>
</body>
</html>
"""


def main():
    if "--help" in sys.argv:
        print(__doc__)
        return

    # posts/ フォルダがなければ作る
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    md_files = [f for f in os.listdir(POSTS_DIR) if f.endswith(".md")]
    if not md_files:
        print("posts/ にMarkdownファイルがありません。")
        return

    all_posts = []

    for filename in md_files:
        filepath = os.path.join(POSTS_DIR, filename)
        slug = filename[:-3]  # .md を除いたファイル名がURL slug

        with open(filepath, encoding="utf-8") as f:
            raw = f.read()

        meta, body_md = parse_frontmatter(raw)

        # Markdown → HTML（コードブロック対応）
        body_html = markdown2.markdown(
            body_md,
            extras=["fenced-code-blocks", "header-ids"]
        )

        # 記事ページを出力
        post_dir = os.path.join(OUTPUT_DIR, slug)
        os.makedirs(post_dir, exist_ok=True)
        out_path = os.path.join(post_dir, "index.html")

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(build_post_html(meta, body_html, slug))

        print(f"  生成: {out_path}")

        all_posts.append({
            "slug":        slug,
            "title":       meta.get("title",          "無題"),
            "title_en":    meta.get("title_en",       meta.get("title", "Untitled")),
            "date":        meta.get("date",            ""),
            "tags":        meta.get("tags",            ""),
            "description": meta.get("description",    ""),
            "description_en": meta.get("description_en", meta.get("description", "")),
        })

    # 新しい順にソート
    all_posts.sort(key=lambda p: p["date"], reverse=True)

    # 一覧ページを出力
    index_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(build_index_html(all_posts))

    print(f"  生成: {index_path}")
    print(f"\n完了！{len(all_posts)} 件の記事をビルドしました。")


if __name__ == "__main__":
    main()
