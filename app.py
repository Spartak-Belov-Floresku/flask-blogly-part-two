from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flask_user:password@localhost/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = 'hello'
app.debug = True
DebugToolbarExtension(app)


@app.route('/')
def home_page():
    """List all users"""

    return redirect('/users')


@app.route('/users')
def list_users():
    """List all users"""

    users = User.query.all()
    return render_template('list_users.html', users = users)


@app.route('/users/new')
def add_form_user():
    """Show form to create a new user"""

    return render_template('form_user.html')


@app.route('/users/new', methods=['POST'])
def add_user():
    """Add a new user to the database"""

    """get data from POST request"""
    first_name = request.form.get('first_name', 'empty')
    last_name = request.form.get('last_name', 'empty')
    img_url = request.form.get('img_url', 'empty')

    """create User object"""
    user = User(first_name=first_name, last_name=last_name, image_url=img_url)

    """Add new objects to session, so they'll persist"""
    db.session.add(user)

    """Commit--otherwise, this never gets saved!"""
    db.session.commit()

    return redirect('/users')


@app.route("/users/<int:id>")
def data_user(id):
    """Show a user page"""

    """Get user from db"""
    user = User.query.get(id)

    return render_template('user.html', user=user)


@app.route('/users/<int:id>/edit')
def edit_form(id):
    """Show an edit user form"""

    """Get user from db"""
    user = User.query.get(id)

    return render_template('edit.html', user=user)


@app.route('/users/<int:id>/edit', methods=['POST'])
def edit_user(id):
    """Update user data"""

    """get user from db"""
    user = User.query.get(id)

    """get data from form"""
    first_name = request.form.get('first_name', 'empty')
    last_name = request.form.get('last_name', 'empty')
    image_url = request.form.get('img_url', 'empty')

    """update user data"""
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()


    return redirect('/users')


@app.route('/users/<int:id>/delete', methods=['POST'])
def delete_user(id):

    """Delete user data from database"""

    User.query.filter_by(id=id).delete()
    db.session.commit()

    return redirect('/users')




@app.route('/users/<int:id>/posts/new')
def add_form_post(id):

    """Show form to add a post for that user"""
    user = User.query.get(id)

    return render_template('form_post.html', user=user)


@app.route('/users/<int:id>/posts/new', methods=['POST'])
def add_user_post(id):
    """Handle add form; add post and redirect to the user detail page"""

    """get data from form"""
    title = request.form.get('title', 'empty')
    content = request.form.get('content', 'empty')

    """Create a new post"""
    post = Post(title=title, content=content, user_id = id)

    db.session.add(post)
    db.session.commit()


    return redirect(f'/users/{id}')


@app.route('/posts/<int:id>')
def show_post(id):
    """Show a post."""

    post = Post.query.get(id)

    return render_template('show_post.html', post=post)


@app.route('/posts/<int:id>/edit')
def edit_post_form(id):
    """Show form to edit a post, and to cancel (back to user page)"""

    """Get user from db"""
    post = Post.query.get(id)

    return render_template('edit_post.html', post=post)


@app.route('/posts/<int:id>/edit', methods=['POST'])
def edit_user_post(id):
    """Handle editing of a post. Redirect back to the post view."""

    """get post from db"""
    post = Post.query.get(id)

    """get data from form"""
    title = request.form.get('title', 'empty')
    content = request.form.get('content', 'empty')

    """update post data"""
    post.title = title
    post.content = content

    db.session.add(post)
    db.session.commit()


    return redirect(f'/posts/{id}')


@app.route('/posts/<int:id>/delete', methods=['POST'])
def delete_post(id):

    """Delete the post."""
    post = Post.query.get(id)
    user_id = post.user_id

    Post.query.filter_by(id=id).delete()
    db.session.commit()

    return redirect(f'/users/{user_id}')



if __name__ == "__main__":
    app.run(debug=True)

