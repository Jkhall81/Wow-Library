<img style='width: 50%' src='https://github.com/Jkhall81/Wow-Library/blob/main/static/WowL.JPG' alt='website image'>
 
 # Wow-Library

## Google Books API Flask App

Wow-Library is a Flask application that utilizes the Google Books API to save and browse book data. It allows users to explore a collection of books, view book
details, rate books, and add comments to books. Users must register an account and login to view comments of books. Bootstrap 5 was used for styling.

## Packages

- Flask
- Flask-Login
- Flask-Migrate
- Flask-SQLAlchemy
- Flask-WTF

## Usage

To use the application, follow these steps:

1. Clone the repository:

```commandline
git clone https://github.com/Jkhall81/Wow-Library.git
cd Wow-Library
```

2. Install the required Python packages:

```commandline
pip install -r requirements.txt
```

3. Run the Flask application

```commandline
python app.py
```

4. Access the application in your web browser at `http://localhost:5000`
5. Begin adding books to your collection!

## Features

* User registration and authentication
* User password hashing
* CSRF token form protection
* Use of blueprints to separate routes
* Responsive web design
* Search Google Books API by Book title or ISBN
* Rate books
* See average rating of books(based on user ratings)
* Sort Books by Title or Author
* Search the collection for a specific title
* Leave comments about a specific book
* Click on book image to see details about a book
* SQLite database
* Ability to migrate database changes

## Roadmap

* Add user profiles
* Add a footer
* Add a favorite book list for each user
* Ability to browse other user's book lists
* UI redesign
* Recommended books based on user's book list

## License

This project is licensed under the MIT License.

