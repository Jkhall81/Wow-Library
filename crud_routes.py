from flask import Blueprint, flash, redirect, render_template, request, url_for
from models import Book, Author, db
from sqlalchemy.exc import SQLAlchemyError

crud_bp = Blueprint('crud', __name__)


@crud_bp.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form.get('name')
        birthdate = request.form.get('birthdate')
        date_of_death = request.form.get('date_of_death')

        new_author = Author(name=name, birthdate=birthdate, date_of_death=date_of_death)
        db.session.add(new_author)
        db.session.commit()
        flash('New author added!')
        return redirect('/')
    return render_template('add_author.html')


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


@crud_bp.route('/add_to_library', methods=['POST'])
def add_to_library():
    book_title = request.form.get('book_title')
    book_authors = request.form.get('book_authors')
    book_published_date = request.form.get('book_published_date')
    book_isbn = request.form.get('book_isbn')
    book_description = request.form.get('book_description')
    book_image_link = request.form.get('book_image_link')

    author_names = book_authors.split(',')
    authors = []

    try:
        with db.session.begin_nested():
            for author_name in author_names:
                author = Author.query.filter_by(name=author_name.strip()).first()
                if not author:
                    if not authors:
                        author = Author(name=author_name.strip())
                    else:
                        max_author_id = db.session.query(db.func.max(Author.id)).scalar()
                        new_author_id = max_author_id + 1 if max_author_id else 1
                        author = Author(name=author_name.strip(), id=new_author_id)

                    db.session.add(author)
                authors.append(author)

            db.session.flush()

            new_book = Book(
                title=book_title,
                publication_year=book_published_date,
                isbn=book_isbn,
                description=book_description,
                image_link=book_image_link,
                author_id=authors[0].id if authors else 1
            )

            new_book.authors = authors

            db.session.add(new_book)
            db.session.commit()
            flash('Book added to library successfully!')

    except SQLAlchemyError as e:
        db.session.rollback()
        flash('Error: Could not add book to library.')

    return redirect(url_for('home'))
