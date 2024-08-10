from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

def get_post_by_id(post_id):
    posts = load_posts()
    for index, post in enumerate(posts):
        if post['id'] == post_id:
            return index, post
    return None, None


#Load blog posts from JSON file
def load_posts():
    with open("posts.json", "r") as fileobj:
        return json.load(fileobj)  # Should return a list of dictionaries

# Function to save blog posts to the JSON file
def save_posts(posts):
    with open('posts.json', 'w') as f:
        json.dump(posts, f, indent=4)
        print("Posts saved to posts.json")
        # Debugging: Read and print the content of the file
        with open('posts.json', 'r') as f:
            content = f.read()
            print("Content of posts.json after save:", content)


@app.route('/')
def index():
    blog_posts = load_posts()  # Fetch the blog posts from the JSON file
    print(blog_posts)  # Debug: Print the blog posts to console/log
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        posts = load_posts()
        new_id = max(post['id'] for post in posts) + 1 if posts else 1
        new_post = {
            'id': new_id,
            'author': request.form['author'],
            'title': request.form['title'],
            'content': request.form['content']
        }
        posts.append(new_post)
        save_posts(posts)
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    posts = load_posts()  # Load all posts
    index, post = get_post_by_id(post_id)  # Get index and post reference

    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post directly in the list
        posts[index]['author'] = request.form['author']
        posts[index]['title'] = request.form['title']
        posts[index]['content'] = request.form['content']

        print("Posts before saving:", posts)  # Debug: print posts before saving
        save_posts(posts)
        print("Posts after saving:", load_posts())  # Debug: print posts after saving

        return redirect(url_for('index'))

    return render_template('update.html', post=post)




@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    # Load the existing posts
    posts = load_posts()

    # Filter out the post with the given ID
    posts = [post for post in posts if post['id'] != post_id]

    # Save the updated posts back to the JSON file
    save_posts(posts)

    # Redirect to the home page
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)