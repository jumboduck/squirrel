from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, FileField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed, FileRequired


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=1, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Create an Account')


class LoginForm(FlaskForm):
    email = StringField('Email', validators = [
                           DataRequired(), Email()])
    password = PasswordField('Password', validators = [
                             DataRequired(), Length(min = 8)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class NewEntryForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired(), Length(min = 1, max = 30)])
    description = TextAreaField('Description', render_kw={"rows": 5}, validators = [DataRequired(), Length(min = 1, max = 500)])
    rating =  RadioField('Rating', validators=[DataRequired()], choices = [('1','Very Poor'),('2','Poor'),('3','Good'),('4','Very Good'),('5','Outstanding')])
    is_fav = BooleanField('Favorite')
    image = FileField('Image', validators = [FileAllowed(['jpg', 'gif', 'png', 'jpeg'], 'Images only!')])
    tags = StringField('Tags', validators = [Length(min = 1, max = 50)])
    submit = SubmitField('Add Review')

