from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")


class SigninForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired(), EqualTo("pass_check", message='Passwords must match')])
    pass_check = PasswordField("pass_check", validators=[DataRequired()])
    name = StringField("name", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired(), Email()])


class UpdateForm(FlaskForm):
    username = StringField("username")
    password = PasswordField("password", validators=[DataRequired(), EqualTo("pass_check", message='Passwords must match')])
    pass_check = PasswordField("pass_check", validators=[DataRequired()])
    name = StringField("name")
    email = StringField("email")


class PostForm(FlaskForm):
    image_name = StringField("image_name", validators=[DataRequired()])
