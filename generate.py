import os
import markdown

POSTS_DIR = "posts"
TEMPLATE_FILE = "template.html"
BLOG_INDEX = "blog.html"

def load_template():
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        return f.read()

def convert_md_to_html(md_file, template):
    with open(md_file, "r", encoding="utf-8") as f:
        text = f.read()
    html_content = markdown.markdown(
        text, extensions=["fenced_code", "tables", "codehilite", "toc", "nl2br", "footnotes"]
    )
    title = text.splitlines()[0].replace("# ", "").strip()
    final_html = template.replace("{{title}}", title).replace("{{content}}", html_content)
    output_file = md_file.replace(".md", ".html")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_html)
    return os.path.basename(output_file), title

def update_blog_index(posts):
    """Auto-update blog.html post list"""
    with open(BLOG_INDEX, "r", encoding="utf-8") as f:
        html = f.read()

    start_marker = "<ul class=\"post-list\">"
    end_marker = "</ul>"
    start = html.find(start_marker)
    end = html.find(end_marker, start)

    if start == -1 or end == -1:
        print("⚠️ Couldn't find <ul class='post-list'> in blog.html")
        return

    list_items = "\n".join(
        f'  <li><a href="posts/{file}">{title}</a></li>' for file, title in posts
    )

    new_html = (
        html[: start + len(start_marker)]
        + "\n" + list_items + "\n"
        + html[end:]
    )

    with open(BLOG_INDEX, "w", encoding="utf-8") as f:
        f.write(new_html)
    print("✅ blog.html updated.")

def main():
    template = load_template()
    posts = []
    for file in os.listdir(POSTS_DIR):
        if file.endswith(".md"):
            md_path = os.path.join(POSTS_DIR, file)
            html_file, title = convert_md_to_html(md_path, template)
            posts.append((html_file, title))
    update_blog_index(sorted(posts, reverse=True))
    print("✨ Conversion complete.")

if __name__ == "__main__":
    main()
