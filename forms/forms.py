from wtforms import Form, IntegerField, StringField, TextAreaField, PasswordField, validators
from wtforms.validators import Email
from flask_wtf.file import FileField
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()


# <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>


class UserRegistrationForm(Form):
    first_name = StringField('First Name', validators=[validators.InputRequired()])
    last_name = StringField('Last Name', validators=[validators.InputRequired()])
    email = StringField('Email', validators=[validators.InputRequired(), Email()])
    password = PasswordField('Password', validators=[validators.InputRequired(), validators.EqualTo('confirm_password', message='Passwords must match!')])
    confirm_password = PasswordField('Confirm Password', validators=[validators.InputRequired()])
    bio = TextAreaField('Bio')
    profile_image = FileField('Profile Image')


class AddBookForm(Form):
    title = StringField('Title', validators=[validators.InputRequired()])


class LoginForm(Form):
    email = StringField('Email', validators=[validators.InputRequired(), Email()])
    password = PasswordField('Password', validators=[validators.InputRequired()])


class EditUserForm(Form):
    first_name = StringField('First Name', validators=[validators.InputRequired()])
    last_name = StringField('Last Name', validators=[validators.InputRequired()])
    bio = TextAreaField('Bio')
    profile_image = FileField('Profile Image')


class BookCommentForm(Form):
    subject = StringField('Subject', validators=[validators.InputRequired()])
    comment_text = TextAreaField('Comment', validators=[validators.InputRequired()])


class EditCommentForm(Form):
    subject = StringField('Subject', validators=[validators.InputRequired()])
    comment_text = TextAreaField('Comment', validators=[validators.InputRequired()])


class RatingForm(Form):
    value = IntegerField('Rating (0-10)', validators=[validators.InputRequired()])
