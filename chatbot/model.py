from chatbot import db , login_manager
from chatbot import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model , UserMixin):
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(30) , nullable = False )
    email = db.Column(db.String(50) , nullable = False, unique = True )
    password_hash = db.Column(db.String(60) , nullable = False)
    messages = db.relationship('Message', backref='user', lazy=True)
    
    @property
    def password(self):
        return self.password_hash
    
    @password.setter
    def password(self , plain_text_passord):
        self.password_hash = bcrypt.generate_password_hash(plain_text_passord).decode('utf-8')
        
    def check_password_correction(self , attempted_password):
        return bcrypt.check_password_hash(self.password_hash , attempted_password)
    


             
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content_user = db.Column(db.String , nullable=True)
    content_chatbot = db.Column(db.String , nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)