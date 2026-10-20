
from flask import Flask, request, jsonify, Response
import markdown
import html
from functools import wraps

app = Flask("hate-secureblog")

# Security fix: reject request bodies larger than 1 MiB.
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024
# Hardcoded authentication token
AUTH_TOKEN = "my-secret-token"

# In-memory storage
posts = {}
next_post_id = 1


def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")

        if token != f"Bearer {AUTH_TOKEN}":
            return jsonify({"error": "Unauthorized"}), 401

        return func(*args, **kwargs)

    return wrapper


@app.route("/posts", methods=["POST"])
@require_auth
def create_post():
    global next_post_id

    # Intentionally no request body size limit
    content = request.get_data(as_text=True)

    post_id = next_post_id
    posts[post_id] = content
    next_post_id += 1

    return jsonify({
        "id": post_id,
        "message": "Post created successfully"
    }), 201


@app.route("/posts/<int:post_id>", methods=["GET"])
@require_auth
def get_post(post_id):
    if post_id not in posts:
        return jsonify({"error": "Post not found"}), 404

    content = posts[post_id]

    # Security fix: escape raw HTML to prevent Stored XSS.
    # Markdown formatting is still converted into HTML.
    safe_content = html.escape(content)
    html_output = markdown.markdown(safe_content)

    return Response(html_output, mimetype="text/html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
