from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint

db = SQLAlchemy()

author_book_association = db.Table(
    'author_book_association',
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True)
)


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

    def __repr__(self):
        return f'Book(isbn={self.isbn}, title={self.title}, publication_year={self.publication_year}, author_id={self.author_id})'


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    __table_args__ = (CheckConstraint('value >= 0 AND value <= 10'),)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

    def __repr__(self):
        return f'Rating(value={self.value}, book_id={self.book_id})'


user_book_association = db.Table(
    'user_book_association',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True)
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    books = db.relationship('Book', secondary=user_book_association, backref=db.backref('users', lazy='dynamic'))
