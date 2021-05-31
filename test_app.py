from unittest import TestCase

from app import app
from models import db, User, Post


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flask_user:password@localhost/blogly_test'
app.config['SQLALCHEMY_ECHO'] = False


app.config['TESTING'] = True


app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Pets."""

    def setUp(self):
        """Add sample pet."""

        Post.query.delete()
        User.query.delete()

        user = User(first_name="Tom", last_name="Smith")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        post = Post(title='New post', content='Some content', user_id = user.id)
        
        db.session.add(post)
        db.session.commit()


        self.post_id = post.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    """run test to get all users"""
    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Tom', html)

    """run test to get user page"""
    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h4 class="mb-0 mt-0">Tom Smith</h4>', html)

    """run test to create a new user in database"""
    def test_add_user(self):
        with app.test_client() as client:
            user = {'first_name': 'John', 'last_name': 'Smith'}
            resp = client.post('/users/new', data=user, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('John Smith', html)


    """run test to change user's data in database"""
    def test_edit_user(self):
        with app.test_client() as client:
            user = {'first_name': 'Tom', 'last_name': 'Walker'}
            resp = client.post(f'/users/{self.user_id}/edit', data=user, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Tom Walker', html)


    """run test to get all postes for user"""
    def test_list_posts_for_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('New post', html)

    """run test to get post page"""
    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p>Some content</p>', html)

    
    """run test to create a new post in database"""
    def test_add_post(self):
        with app.test_client() as client:
            post = {'title': 'Secon title', 'content': 'Second content', 'user_id': self.user_id}
            resp = client.post(f'/users/{self.user_id}/posts/new', data=post, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Secon title', html)

    """run test to change post's data in database"""
    def test_edit_post(self):
        with app.test_client() as client:
            post = {'title': 'Change post title', 'content': 'Change post content'}
            resp = client.post(f'/posts/{self.post_id}/edit', data=post, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Change post title', html)