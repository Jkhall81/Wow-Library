from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user
from models import Book, Author, db
from sqlalchemy.exc import SQLAlchemyError

crud_bp = Blueprint('crud', __name__)


@crud_bp.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        author_id = request.form.get('author_id')
        isbn = request.form.get('isbn')
        title = request.form.get('title')
        publication_year = request.form.get('publication_year')

        new_book = Book(isbn=isbn, title=title, publication_year=publication_year, author_id=author_id)
        db.session.add(new_book)
        db.session.commit()
        flash('New book added!')
    return render_template('add_book.html')


@crud_bp.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        flash('Book deleted successfully')
    else:
        flash('Book not found!')
    return redirect(url_for('home'))


@crud_bp.route('/my_books/<int:user_id>', methods=['POST', 'GET'])
def my_books():
    return render_template('my_books.html')
