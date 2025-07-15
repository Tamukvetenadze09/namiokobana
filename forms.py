from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email, InputRequired, length


class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=20)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Enter password", validators=[DataRequired(),
                                                             length(min=8, max=32)])
    confirm_password = PasswordField("Confirm password",
                                     validators=[DataRequired(), EqualTo("password", message="Passwords must match")])
    birthdate = DateField("Birthdate", validators=[DataRequired()])
    country = SelectField("Country", validators=[InputRequired()], choices=[
        ("", "Choose country"),
        ("ge", "Georgia"),
        ("it", "Italy"),
        ("fr", "France"),
        ("es", "Spain")
    ])
    gender = SelectField("Gender", choices=[
        ("male", "Male"),
        ("female", "Female")
    ], validators=[DataRequired()])
    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class TeamForm(FlaskForm):
    team1 = StringField("გუნდი 1", validators=[DataRequired()])
    team2 = StringField("გუნდი 2", validators=[DataRequired()])
    submit = SubmitField("დაწყება")


class PlayForm(FlaskForm):
    guessed = SubmitField("გამოიცნო")
    not_guessed = SubmitField("ვერ გამოიცნო")




class AddWordForm(FlaskForm):
    text = StringField("შეიყვანე სიტყვა", validators=[
        DataRequired(message="გთხოვ შეიყვანე სიტყვა."),
        Length(min=2, max=100, message="სიტყვა უნდა იყოს 2-100 სიმბოლო.")
    ])
    submit = SubmitField("დამატება")

