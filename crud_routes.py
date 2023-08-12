from datamanager.sqlalchemy_data_manager import SQAlchemyDataManager
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user
from forms.forms import AddBookForm
from models import Book, db

crud_bp = Blueprint('crud', __name__)
data_manager = SQAlchemyDataManager('data/library.sqlite')


@crud_bp.route('/add_book/<int:user_id>', methods=['GET', 'POST'])
def add_book(user_id):
    form = AddBookForm()
    if request.method == 'POST' and form.validate():
        isbn = request.form.get('isbn')
        title = request.form.get('title')

        api_params = {
            'key': data_manager.api_key
        }

        if isbn:
            api_params['q'] = f'isbn:{isbn}'
        elif title:
            api_params['q'] = f'title:{title}'

        new_book = data_manager.add_book(user_id, api_params)
        if new_book == 200:
            flash('New book successfully added!')
            return redirect(url_for('crud.my_books', user_id=current_user.id))

    return render_template('add_book.html', form=form)


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
def my_books(user_id):
    books = data_manager.get_user_books(user_id)
    return render_template('my_books.html', books=books)
