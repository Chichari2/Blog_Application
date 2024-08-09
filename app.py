from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

#Load blog posts from JSON file
def load_posts():
    with open("posts.json", "r") as fileobj:
        return json.load(fileobj)

@app.route('/')
def index():
    blog_posts = load_posts()  # Fetch the blog posts from the JSON file
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(debug=True)