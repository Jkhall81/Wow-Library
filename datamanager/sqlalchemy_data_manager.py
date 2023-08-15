from models import User, Book, Author, Comment, Rating, db
import config
import requests


class SQAlchemyDataManager():
    def __init__(self, db_file_name):
        self.db = db
        self.api_key = 'AIzaSyDd7MoNSm_LrRzR9keXv_nQcNC4XYXHvPI'

    def add_author(self, author_name):
        author = Author.query.filter_by(name=author_name).first()
        if author:
            return author.id
        else:
            new_author = Author(name=author_name)
            db.session.add(new_author)
            db.session.commit()
            return new_author.id

    def get_all_users(self):
        users = User.query.all()
        return users

    def get_user_books(self, user_id):
        books = Book.query.filter_by(user_id=user_id)
        return books

    def add_user(self, first_name, last_name, email, password, bio, profile_image=None):
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=password, bio=bio)
        if profile_image:
            new_user.profile_image = profile_image
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def add_book(self, user_id, params):
        response = requests.get('https://www.googleapis.com/books/v1/volumes', params=params)

        if response.status_code == 200:
            data = response.json()
            print(data)

            # maybe in the future i want to give the user a list of books and they can choose which to add, for now just one book
            books = []
            for item in data.get('items', []):
                volume_info = item.get('volumeInfo', {})
                image_links = volume_info.get('imageLinks', {})
                book = {
                    'title': volume_info['title'],
                    'authors': volume_info.get('authors', ['N/A']),
                    'published_date': volume_info.get('publishedDate', 'N/A'),
                    'isbn': volume_info.get('industryIdentifiers', [{}])[0].get('identifier', 'N/A'),
                    'image_link': image_links.get('thumbnail', None),
                    'description': volume_info.get('description', 'N/A'),
                }
                books.append(book)
            first_book = books[0]

            # get an author_id
            author = first_book['authors'][0]
            author_id = self.add_author(author)

            # add the book to the database
            new_book = Book(isbn=first_book['isbn'], title=first_book['title'], publication_year=first_book['published_date'],
                            description=first_book['description'], image_link=first_book['image_link'], author_id=author_id,
                            user_id=user_id)

            # save this bad boy
            if new_book:
                db.session.add(new_book)
                db.session.commit()
                return new_book

    def delete_book(self, book_id):
        try:
            book = Book.query.filter_by(id=book_id).first()
            if book:
                db.session.delete(book)
                db.session.commit()
            else:
                raise ValueError('Book not found')
        except ValueError as e:
            db.session.rollback()
            print('An error occurred:', str(e))

    def save_rating(self, value, book_id):
        new_rating = Rating(value=value, book_id=book_id)
        if new_rating:
            db.session.add(new_rating)
            db.session.commit()
            return 200

    def average_rating(self, book_id):
        ratings = Rating.query.filter_by(book_id=book_id).all()
        if not ratings:
            return None
        total_ratings = sum(rating.value for rating in ratings)
        average_rating = total_ratings / len(ratings)
        return average_rating

    def add_comment(self, subject, comment_text, book_id, user_id):
        new_comment = Comment(subject=subject, comment_text=comment_text, book_id=book_id, user_id=user_id)
        if new_comment:
            db.session.add(new_comment)
            db.session.commit()
            return new_comment

    def get_name(self, user_id):
        user = User.query.get(user_id)
        if user:
            return user.first_name, user.last_name
