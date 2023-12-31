from datamanager.sqlalchemy_data_manager import SQAlchemyDataManager
from flask import Blueprint, flash, redirect, render_template, request, send_from_directory, url_for
from flask_login import current_user
from forms.forms import AddBookForm, RatingForm, BookCommentForm, EditCommentForm
from models import Book, Comment, User, db

crud_bp = Blueprint('crud', __name__)
data_manager = SQAlchemyDataManager('data/library.sqlite')


@crud_bp.route('/add_book/<int:user_id>', methods=['GET', 'POST'])
def add_book(user_id):
    form = AddBookForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data

        api_params = {
            'key': data_manager.api_key
        }

        if title:
            api_params['q'] = f'title:{title}'

        new_book = data_manager.add_book(user_id, api_params)
        if new_book:
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
    return redirect(url_for('crud.my_books', user_id=current_user.id))


@crud_bp.route('/my_books/<int:user_id>', methods=['POST', 'GET'])
def my_books(user_id):
    form = RatingForm()
    books = data_manager.get_user_books(user_id)

    average_ratings = {}

    for book in books:
        average_ratings[book.id] = data_manager.average_rating(book.id)

    return render_template('my_books.html', books=books, form=form, average_ratings=average_ratings)


@crud_bp.route('/rate_book/<int:book_id>', methods=['POST', 'GET'])
def rate_book(book_id):
    if request.method == 'POST':
        value = float(request.form['rating'])

        added_rating = data_manager.save_rating(value, book_id)
        if added_rating == 200:
            flash('Rating successfully submitted!')
            return redirect(url_for('crud.my_books', user_id=current_user.id))

    return redirect(url_for('crud.my_books', user_id=current_user.id))


@crud_bp.route('/book_details/<int:book_id>', methods=['POST', 'GET'])
def book_details(book_id):
    book = Book.query.filter_by(id=book_id).first()
    form = BookCommentForm(request.form)
    comments = Comment.query.filter_by(book_id=book_id).all()
    if request.method == 'POST' and form.validate():
        subject = form.subject.data
        comment_text = form.comment_text.data

        new_comment = data_manager.add_comment(subject, comment_text, book_id, current_user.id)
        if new_comment:
            flash('Comment successfully submitted!')
            return redirect(url_for('crud.book_details', book_id=book.id, book=book, form=form, comments=comments))

    comments_with_user_info = []
    for comment in comments:
        # watch me work
        user = User.query.get(comment.user_id)
        comments_with_user_info.append({
            'comment': comment,
            'user': user,
        })

    return render_template('book_details.html', book=book, form=form, comments=comments_with_user_info)


@crud_bp.route('/edit_comment/<int:comment_id>', methods=['POST', 'GET'])
def edit_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    form = EditCommentForm(request.form)
    print(comment.comment_text)

    # I'm too lazy to make a function for this, its not much code anyway
    if request.method == 'POST' and form.validate():
        comment.subject = form.subject.data
        comment.comment_text = form.comment_text.data

        db.session.commit()
        flash('Comment successfully updated!')
        return redirect(url_for('crud.book_details', book_id=comment.book_id))

    return render_template('edit_comment.html', comment_id=comment_id, form=form, comment=comment)


@crud_bp.route('/all_users')
def all_users():
    users = data_manager.get_all_users()
    return render_template('all_users.html', users=users)


@crud_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)
