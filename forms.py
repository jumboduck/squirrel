from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, TextAreaField, HiddenField
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


class EntryForm(FlaskForm):
    name = TextAreaField('Name', render_kw={"rows": 1, "spellcheck":"false", "maxlength":30, "data-expandable":"true"}, validators = [DataRequired(), Length(min = 1, max = 30)])
    description = TextAreaField('Description', render_kw={"spellcheck":"false", "maxlength":2000, "rows":1, "data-expandable":"True"}, validators = [DataRequired(), Length(min = 1, max = 2000)])
    rating =  RadioField('Rating', validators=[DataRequired()], choices = [('5','Outstanding'),('4','Very Good'),('3','Good'),('2','Poor'), ('1','Very Poor')])
    is_fav = BooleanField('Favorite')
    image = FileField('Image', render_kw={"accept":"image/*", "capture":"environment"} ,validators = [FileAllowed(['jpg', 'gif', 'png', 'jpeg'], 'Images only!')])
    tags = StringField('Tags', validators = [Length(min=0, max = 100)])
    hidden_tags = HiddenField('Hidden Tags', validators = [Length(min = 0, max = 100)])
    hidden_id = HiddenField('Hidden Id')

class NewEntryForm(FlaskForm):
    name = TextAreaField('Name', render_kw={"rows": 1, "spellcheck":"false", "maxlength":30}, validators = [DataRequired(), Length(min = 1, max = 30)])
    description = TextAreaField('Description', render_kw={"rows": 5, "spellcheck":"false", "maxlength":2000}, validators = [DataRequired(), Length(min = 1, max = 2000)])
    rating =  RadioField('Rating', validators=[DataRequired()], choices = [('5','Outstanding'),('4','Very Good'),('3','Good'),('2','Poor'), ('1','Very Poor')])
    is_fav = BooleanField('Favorite')
    image = FileField('Image', render_kw={"accept":"image/*", "capture":"environment"}, validators = [FileAllowed(['jpg', 'gif', 'png', 'jpeg'], 'Only image files can be uploaded.')])
    hidden_tags = HiddenField('Hidden Tags')
    submit = SubmitField('Add Review')

