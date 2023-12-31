from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint

db = SQLAlchemy()


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    birthdate = db.Column(db.String)
    date_of_death = db.Column(db.String)

    def __repr__(self):
        return f'author(name={self.name}, birthdate={self.birthdate}, date_of_death={self.date_of_death})'


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    image_link = db.Column(db.String)
    ratings = db.relationship('Rating', backref='book', lazy=True)
    author = db.relationship('Author', backref='books')
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Book(isbn={self.isbn}, title={self.title}, publication_year={self.publication_year}, author_id={self.author_id})'


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    __table_args__ = (CheckConstraint('value >= 0 AND value <= 10'),)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

    def __repr__(self):
        return f'Rating(value={self.value}, book_id={self.book_id})'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    bio = db.Column(db.Text)
    profile_image = db.Column(db.String(255))

    def __repr__(self):
        return f'User(first_name={self.first_name}, last_name={self.last_name})'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.Text, nullable=False)
    comment_text = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

    def __repr__(self):
        return f'Comment(id={self.id}, comment_text={self.comment_text})'
