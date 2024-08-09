from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

#Load blog posts from JSON file
def load_posts():
    with open("posts.json", "r") as fileobj:
        return json.load(fileobj)

# Function to save blog posts to the JSON file
def save_posts(posts):
    with open('posts.json', 'w') as f:
        json.dump(posts, f, indent=4)

@app.route('/')
def index():
    blog_posts = load_posts()  # Fetch the blog posts from the JSON file
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Get data from the form
        new_post = {
            'id': len(load_posts()) + 1,
            'author': request.form['author'],
            'title': request.form['title'],
            'content': request.form['content']
        }
        # Load existing posts, add the new post, and save them back to the JSON file
        posts = load_posts()
        posts.append(new_post)
        save_posts(posts)

        # Redirect to the home page after adding the post
        return redirect(url_for('index'))

    # If GET request, display the add form
    return render_template('add.html')


if __name__ == '__main__':
    app.run(debug=True)