from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from application.models import User
class LoginForm(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Email()])
    password=StringField("Password",validators=[DataRequired(),Length(min=6,max=15)])
    remember_me=BooleanField("Remember me")
    submit=SubmitField("Login")

class RegisterForm(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Email()])
    password=StringField("Password",validators=[DataRequired(),Length(min=6,max=15)])
    password_confirm=StringField("Confirm Password",validators=[DataRequired(),Length(min=6,max=15),EqualTo('password')])
    first_name=StringField("Name",validators=[DataRequired(),Length(min=1,max=75)])
    last_name=StringField("Family name",validators=[DataRequired(),Length(min=1,max=75)])
    submit=SubmitField("Register")

    def validate_email(self,email):
        user=User.objects(email=email.data).first()
        if user:
            raise ValidationError("Email is already in use. Pick another one.")

