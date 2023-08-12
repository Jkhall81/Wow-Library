from auth import auth
from crud_routes import crud_bp
from flask import Flask, flash, render_template, redirect, request, url_for
from flask_login import current_user, LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from models import Book, Comment, Rating, User, db
import config
import requests


def average(values):
    if not values:
        return None
    return sum(values) / len(values)


app = Flask(__name__)
app.jinja_env.filters['average'] = average
app.config.from_object(config)
migrate = Migrate(app, db)
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(crud_bp, url_prefix='/crud')
db.init_app(app)
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# Routes

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    #     print(' * Database created successfully!')
    app.run(debug=True)
