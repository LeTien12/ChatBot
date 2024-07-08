from flask import Flask , render_template
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_ngrok import run_with_ngrok

from pyngrok import ngrok





app = Flask(__name__)

# ngrok.set_auth_token('2a4sPVXInxRnuXiVtqvAXOPRmVU_2d8Gd8398dweN2odJtUWr')

# public_url = ngrok.connect(5000).public_url

# print(f" * ngrok tunnel {public_url}")


app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.abspath('./chatbot/chatbot.db')}"
app.config['SECRET_KEY'] = 'a1cb52afdb4accaf3465d6d4'


db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'


from chatbot import route








    



    