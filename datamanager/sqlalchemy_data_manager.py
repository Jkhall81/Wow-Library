from models import User, Book, Comment, Rating, db
import requests


class SQAlchemyDataManager():
    def __init__(self, db_file_name):
        self.db = db
        self.api_key = 'AIzaSyDd7MoNSm_LrRzR9keXv_nQcNC4XYXHvPI'

    def get_all_users(self):
        users = User.query.all()
        return users

    def get_user_books(self, user_id):
        books = Book.query.filter_by(user_id=user_id)
        return books

    def add_user(self, first_name, last_name, email, password, bio):
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=password, bio=bio)
        db.session.add(new_user)
        db.session.commit()

    def add_book(self, params):
        response = requests.get('https://www.googleapis.com/books/v1/volumes', params=params)

        if response.status_code == 200:
            data = response.json()

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
            return books

    def delete_book(self, book_id, user_id):
        try:
            book = Book.query.filter_by(user_id=user_id, id=book_id).first()
            if book:
                db.session.delete(book)
                db.session.commit()
            else:
                raise ValueError('Book not found')
        except ValueError as e:
            db.session.rollback()
            print('An error occurred:', str(e))
