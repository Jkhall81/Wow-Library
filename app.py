from crud_routes import crud_bp
from flask import Flask, flash, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from models import Author, Book, Rating, db
import config
import requests


def average(values):
    if not values:
        return None
    return sum(values) / len(values)


app = Flask(__name__)
app.jinja_env.filters['average'] = average
app.config.from_object(config)
app.register_blueprint(crud_bp, url_prefix='/crud')
db.init_app(app)
API_KEY = 'AIzaSyDd7MoNSm_LrRzR9keXv_nQcNC4XYXHvPI'
csrf = CSRFProtect(app)


# Routes

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        search_query = request.form.get('search_query')

        if search_query:
            books = Book.query.filter(
                (Book.title.contains(search_query)) |
                (Book.description.contains(search_query))
            ).all()
        else:
            books = Book.query.all()

    else:
        books = Book.query.all()

    # get average rating
    for book in books:
        total_ratings = len(book.ratings)
        if total_ratings > 0:
            sum_ratings = sum(rating.value for rating in book.ratings)
            average_rating = sum_ratings / total_ratings
            book.average_rating = average_rating
        else:
            book.average_rating = 0

    return render_template('home.html', books=books)


@app.route('/search', methods=['GET', 'POST'])
def search_books():
    if request.method == 'POST':
        search_term = request.form.get('search_term')
        isbn = request.form.get('isbn')

        if isbn:
            params = {'q': 'isbn:' + isbn, 'key': API_KEY}
        else:
            params = {'q': 'intitle:' + search_term, 'key': API_KEY}

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

            return render_template('search_results.html', books=books)
        else:
            return 'Error occurred while fetching data from Google Books API.'
    else:
        return render_template('search_form.html')


@app.route('/sort_by_title')
def sort_by_title():
    books = Book.query.order_by(Book.title).all()
    return render_template('home.html', books=books)


@app.route('/sort_by_author')
def sort_by_author():
    books = Book.query.join(Book.author).order_by(Author.name).all()
    return render_template('home.html', books=books)


@app.route('/rate_book/<int:book_id>', methods=['GET', 'POST'])
def rate_book(book_id):
    book = Book.query.get_or_404(book_id)

    if request.method == 'POST':
        rating_value = int(request.form.get('rating'))
        rating = Rating(value=rating_value, book_id=book.id)
        db.session.add(rating)
        db.session.commit()

    return redirect(url_for('home'))


@app.route('/book_details/<int:book_id>')
def book_details(book_id):
    book = Book.query.get_or_404(book_id)

    return render_template('book_details.html', book=book)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()