from flask import Flask, render_template
import os, markdown, datetime

app = Flask(__name__)

BLOG_DIR = "blogs"

@app.route("/")
def home():
    files = os.listdir(BLOG_DIR)
    posts = []

    for file in files:
        if file.endswith(".md"):
            slug = file.replace(".md", "")
            date = datetime.datetime.fromtimestamp(
                os.path.getctime(f"{BLOG_DIR}/{file}")
            ).strftime("%d %b %Y")

            with open(f"{BLOG_DIR}/{file}", "r", encoding="utf-8") as f:
                content = f.read()
                preview = content[:120] + "..."

            posts.append({"slug": slug, "date": date, "preview": preview})

    return render_template("index.html", posts=posts)

@app.route("/blog/<slug>")
def post(slug):
    try:
        with open(f"{BLOG_DIR}/{slug}.md", "r", encoding="utf-8") as f:
            content = f.read()
        html = markdown.markdown(content)
        date = datetime.datetime.fromtimestamp(
            os.path.getctime(f"{BLOG_DIR}/{slug}.md")
        ).strftime("%d %b %Y")

        return render_template("post.html", title=slug, content=html, date=date)
    except:
        return "Blog not found", 404

if __name__ == "__main__":
    app.run(debug=True)

