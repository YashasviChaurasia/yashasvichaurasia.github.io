import os
import markdown
from datetime import datetime
from pathlib import Path

POSTS_DIR = "posts"
TEMPLATE_FILE = "template.html"
BLOG_INDEX = "blog.html"

def load_template():
    """Load the HTML template used for each post."""
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        return f.read()

def convert_md_to_html(md_file, template):
    """Convert a markdown file into an HTML file using the template."""
    with open(md_file, "r", encoding="utf-8") as f:
        text = f.read()

    html_content = markdown.markdown(
        text,
        extensions=["fenced_code", "tables", "footnotes", "nl2br"]
    )

    # The first line (usually '# Title') becomes the post title
    title = text.splitlines()[0].replace("# ", "").strip()
    output_file = md_file.replace(".md", ".html")

    # Fill the template placeholders
    final_html = (
        template
        .replace("{{title}}", title)
        .replace("{{content}}", html_content)
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_html)

    return os.path.basename(output_file), title

def generate_blog_index(posts):
    """Generate a minimal, elegant blog index with bullet points and no dates."""
    post_items = []
    for file, title in posts:
        post_items.append(f'  <li><a href="posts/{file}">{title}</a></li>')

    post_list_html = "\n".join(post_items)

    blog_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Writing — Yashasvi Chaurasia</title>
  <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500&family=Inter:wght@300;400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <main>
    <header>
      <h1>Writing</h1>
      <p class="subtitle">fragments, reflections, and notes</p>
    </header>

    <section>
      <ul class="post-list">
{post_list_html}
      </ul>
    </section>

    <nav>
      <a href="index.html" class="back-home">← back home</a>
    </nav>
  </main>
</body>
</html>"""

    with open(BLOG_INDEX, "w", encoding="utf-8") as f:
        f.write(blog_html)

    print(f"✅ blog.html updated with {len(posts)} posts.")


def main():
    template = load_template()
    posts = []

    # Convert all markdown files to HTML
    for file in os.listdir(POSTS_DIR):
        if file.endswith(".md"):
            md_path = os.path.join(POSTS_DIR, file)
            html_file, title = convert_md_to_html(md_path, template)
            posts.append((html_file, title))

    # Sort by filename or modification time (latest first)
    posts_sorted = sorted(posts, key=lambda x: os.path.getmtime(os.path.join(POSTS_DIR, x[0])), reverse=True)
    generate_blog_index(posts_sorted)

    print("✨ Conversion complete.")

if __name__ == "__main__":
    main()
