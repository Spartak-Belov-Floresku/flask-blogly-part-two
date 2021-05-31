from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, sql

db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""
    
    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    image_url = db.Column(db.String(250), nullable=False, default="empty")


    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __repr__(self):
        return f'<User id: {self.id} - {self.first_name} {self.last_name}>'


class Post(db.Model):

    __tablename__= 'post'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(125), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(DateTime(timezone=True), default=sql.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user =  db.relationship('User', backref = 'posts')


    def __repr__(self):
        return f'<Post id: {self.id} - created adte {self.created_at} user: {User.first_name}>'