from datamanager.sqlalchemy_data_manager import SQAlchemyDataManager
from flask import Blueprint, render_template, request, flash, redirect, url_for
from forms.forms import UserRegistrationForm, LoginForm
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from models import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)
data_manager = SQAlchemyDataManager('data/library.sqlite')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('logged in successfully!')
                login_user(user, remember=True)
                return redirect(url_for('home', user=user))
            else:
                flash('Incorrect password, try again.')

        else:
            flash('Email does not exist.')

    return render_template('login.html', user=current_user, form=form)


@auth.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('You have been successfully logged out!')
    return redirect(url_for('home'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    user = current_user
    form = UserRegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        bio = form.bio.data

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.')
        elif password != confirm_password:
            flash('Passwords don\'t match.')
        else:
            new_user = data_manager.add_user(first_name, last_name, email, password=generate_password_hash(password, method='sha256'), bio=bio)
            login_user(new_user, remember=True)
            flash('Account created!')
            return redirect(url_for('home', user=user))

    return render_template('sign_up.html', user=user, form=form)
