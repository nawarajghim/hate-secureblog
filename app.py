
from flask import Flask, request, jsonify, Response
import markdown
from functools import wraps

app = Flask("hate-secureblog")

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

    # Intentionally unsafe Markdown rendering:
    # raw HTML is preserved without sanitization.
    html = markdown.markdown(content)

    return Response(html, mimetype="text/html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
