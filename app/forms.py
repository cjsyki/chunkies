from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField, IntegerField
from wtforms.validators import Length, ValidationError, Email, EqualTo, DataRequired
from app.models import User

# login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

# registration form
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

# coordinates form (stores coordinates for routes.py to retrieve)
# not the best yet :(, working on it
class SearchForm(FlaskForm):
    zipcode = IntegerField('Zipcode', validators=[DataRequired()])
    options = RadioField('Options', choices=[('breakfast', 'breakfast'), ('lunch','lunch'), ('dinner', 'dinner'), ('dessert', 'dessert')], \
                validators=[DataRequired()])
    submit = SubmitField('Click here to continue')
    def validate_zipcode(self, zipcode):
        try:
            newZip = int(str(zipcode.data))
            if newZip < 501 or newZip > 99950:
                raise ValidationError('Please enter a valid zipcode')
        except ValueError:
            raise ValidationError('Please enter a valid zipcode')
