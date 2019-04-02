from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")


class SigninForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    pass_check = PasswordField("pass_check", validators=[DataRequired()])
    name = StringField("name", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])


class PostForm(FlaskForm):
    content = TextAreaField("content", validators=[DataRequired()])
