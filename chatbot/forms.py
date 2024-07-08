from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField
from wtforms.validators import Length , Email , DataRequired

class RegisterForm(FlaskForm):
    username = StringField(label='username' , validators= [Length(min=2 , max=30) , DataRequired()])
    email = StringField(label='email' , validators= [Email() ,DataRequired()])
    password = PasswordField(label='password' , validators= [Length(min=6 , max=30) , DataRequired()])
    submit = SubmitField(label= 'submit')
    
    
class LoginForm(FlaskForm):
    email = StringField(label='email' , validators= [DataRequired()])
    password = PasswordField(label='password' , validators= [DataRequired()])
    submit = SubmitField(label= 'submit')
    
    