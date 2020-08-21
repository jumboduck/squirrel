from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,\
    RadioField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo,\
    Optional, Regexp
from flask_wtf.file import FileField, FileAllowed, FileRequired
from config import text_regex


# The following class creates the a new user registration form
# and defines validation rules for each of its fields
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[
                            DataRequired(),
                            Length(min=1, max=30),
                            Regexp(text_regex, message="Username cannot "
                                                       "start with a space")
                           ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[
                                      DataRequired(),
                                      EqualTo('password')])
    submit = SubmitField('Create an Account')


# The following class creates the form to log into the application
# and defines validation rules for each of its fields
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


# The following class creates the form that will hold the content
# of each entry. Its validation rules are defined here.
class EntryForm(FlaskForm):
    name = TextAreaField('Name',
                         render_kw={"rows": 1,
                                    "spellcheck": "false",
                                    "maxlength": 30,
                                    "data-expandable": "true"},
                         validators=[Regexp(text_regex, message="Name cannot start with a space"),
                                     DataRequired(),
                                     Length(min=1, max=30)])
    description = TextAreaField('Description',
                                render_kw={"spellcheck": "false",
                                           "maxlength": 2000,
                                           "rows": 1,
                                           "data-expandable": "True"},
                                validators=[Regexp(text_regex,
                                                   message=("Description cannot start"
                                                            " with a space or line break")),
                                            DataRequired(),
                                            Length(min=1, max=2000)])
    rating = RadioField('Rating',
                        validators=[DataRequired()],
                        choices=[('5', 'Outstanding'),
                                 ('4', 'Very Good'),
                                 ('3', 'Good'),
                                 ('2', 'Poor'),
                                 ('1', 'Very Poor')])
    is_fav = BooleanField('Favorite')
    image = FileField('Image',
                      render_kw={"accept": "image/*"},
                      validators=[FileAllowed(['jpg', 'gif', 'png', 'jpeg'],
                                  'Images only!')])
    tags = StringField('Tags', validators=[Length(min=0, max=100)])
    hidden_tags = HiddenField('Hidden Tags',
                              validators=[Length(min=0, max=100)])
    hidden_id = HiddenField('Hidden Id')


# The following class creates the form that allows users to add
# a new review and defines validation rules for each of its fields
class NewEntryForm(FlaskForm):
    name = TextAreaField('Name',
                         render_kw={"rows": 1, "spellcheck": "false", "maxlength": 30},
                         validators=[Regexp(text_regex,
                                            message=("Name cannot start with a "
                                                     "space or line break")),
                                     DataRequired(),
                                     Length(min=1, max=30)])
    description = TextAreaField('Description',
                                render_kw={"rows": 5, "spellcheck": "false", "maxlength": 2000},
                                validators=[Regexp(text_regex,
                                                   message="Description cannot start with a "
                                                           "space or line break"),
                                            DataRequired(),
                                            Length(min=1, max=2000)])
    rating = RadioField('Rating',
                        validators=[DataRequired()],
                        choices=[('5', 'Outstanding'),
                                 ('4', 'Very Good'),
                                 ('3', 'Good'),
                                 ('2', 'Poor'),
                                 ('1', 'Very Poor')])
    is_fav = BooleanField('Favorite')
    image = FileField('Image',
                      render_kw={"accept": "image/*"},
                      validators=[FileAllowed(['jpg', 'gif', 'png', 'jpeg'],
                                              'Only image files can be uploaded.')])
    hidden_tags = HiddenField('Hidden Tags')
    submit = SubmitField('Add Review')


# The following class creates the form to update the user's account
# information and defines validation rules for each of its fields
class UpdateAccount(FlaskForm):
    username = StringField('Username',
                           validators=[Length(min=1, max=30), Optional()])
    email = StringField('Email',
                        validators=[Email(), Optional()])
    new_password = PasswordField('New Password',
                                 validators=[Length(min=8), Optional()])
    confirm_password = PasswordField('Confirm New Password',
                                     validators=[EqualTo('new_password')])
    password = PasswordField('Current Password',
                             validators=[DataRequired()])
    submit = SubmitField('Save Changes')
