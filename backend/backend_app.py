from flask import Flask, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
    {"id": 3, "title": "Flask tutorial", "content": "Learn Flask with this tutorial."},
    {"id": 4, "title": "Python basics", "content": "An introduction to Python programming."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    sort_by = request.args.get('sort', default=None, type=str)
    direction = request.args.get('direction', default=None, type=str)

    valid_sort_fields = ["title", "content"]
    valid_directions = ["asc", "desc"]

    if sort_by and sort_by not in valid_sort_fields:
        abort(400, description=f"Invalid sort field. Use one of: {', '.join(valid_sort_fields)}")

    if direction and direction not in valid_directions:
        abort(400, description=f"Invalid sort direction. Use 'asc' or 'desc'.")

    sorted_posts = POSTS.copy()

    if sort_by:
        sorted_posts.sort(key=lambda post: post[sort_by].lower(), reverse=(direction == 'desc'))

    return jsonify(sorted_posts)


@app.route('/api/posts', methods=['POST'])
def create_post():
    new_data = request.get_json()
    if not new_data:
        abort(400, description="No JSON new_data provided.")

    title = new_data.get("title")
    content = new_data.get("content")

    if not title or not content:
        missing_fields = []
        if not title:
            missing_fields.append("title")
        if not content:
            missing_fields.append("content")
        abort(400, description=f"Missing required fields: {', '.join(missing_fields)}")

    # Generate a new ID for the post
    new_id = len(POSTS) + 1

    # Create the new post
    new_post = {"id": new_id, "title": title, "content": content}
    POSTS.append(new_post)

    # Return the new post with the status code 201 Created
    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    # Find the post with the given id
    post_to_delete = next((post for post in POSTS if post["id"] == post_id), None)

    # If the post doesn't exist, return a 404 Not Found response
    if not post_to_delete:
        abort(404, description=f"Post with id {post_id} not found.")

    # Remove the post from the list of posts
    POSTS.remove(post_to_delete)

    # Return a success message with status code 200 OK
    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    new_data = request.get_json()
    if not new_data:
        abort(400, description="No JSON new_data provided.")

    # Find the post with the given id
    post_to_update = next((post for post in POSTS if post["id"] == post_id), None)

    # If the post doesn't exist, return a 404 Not Found response
    if not post_to_update:
        abort(404, description=f"Post with id {post_id} not found.")

    # Update the post with the new new_data (if provided)
    if "title" in new_data:
        post_to_update["title"] = new_data["title"]
    if "content" in new_data:
        post_to_update["content"] = new_data["content"]

    # Return the updated post with the status code 200 OK
    return jsonify(post_to_update), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_query = request.args.get('title', default=None, type=str)
    content_query = request.args.get('content', default=None, type=str)

    matching_posts = []
    for post in POSTS:
        if title_query and title_query.lower() in post["title"].lower():
            matching_posts.append(post)
        elif content_query and content_query.lower() in post["content"].lower():
            matching_posts.append(post)

    return jsonify(matching_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
