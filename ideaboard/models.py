from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from ideaboard import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
     return User.query.get(int(user_id))


''' Database structure for a user '''
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    #comment = db.relationship('Comment', backref='article_1', lazy=True)
    likes = db.relationship('PostLike', foreign_keys='PostLike.user_id',
        backref='user', lazy='dynamic')

    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(user_id=self.id, post_id=post.id).delete()

    def has_liked_post(self, post):
        return PostLike.query.filter(PostLike.user_id == self.id, PostLike.post_id == post.id).count() > 0

    def get_reset_token(self, expires_sec=1800):                #Login expires after 30 mins
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


''' Database structure for a post/idea '''
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    effort_required = db.Column(db.Text, nullable=False)
    business_value = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment = db.relationship('Comment', backref='article', lazy=True)
    likes = db.relationship('PostLike', backref='post', lazy='dynamic')

    #def get_comments(self):
    #    return Comment.query.filter_by(post_id=post.id).order_by(Comment.timestamp.desc())

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


''' Database structure for a comment '''
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    #username = db.Column(db.String(20), db.ForeignKey('username'), unique=True, nullable=False)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Comment('{self.comment}', '{self.username}', '{self.date_posted}')"


''' Database structure for like '''
class PostLike(db.Model):
    __tablename__ = 'post_like'
    id = db.Column(db.Integer, primary_key=True)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

'''
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        #return '<Post %r>' % (self.body)
        return f"Post('{self.body}', '{self.date_posted}')"
'''
'''class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    author = db.Column(db.String(32))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow, index=True)'''