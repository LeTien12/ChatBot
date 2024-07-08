from chatbot import app
from flask import render_template , redirect , url_for,flash , get_flashed_messages,request
from chatbot.forms import RegisterForm ,LoginForm
from chatbot.model import User ,Message
from chatbot import db
from chatbot.chat_model import chat_predict

from flask_login import login_user , logout_user , login_required , current_user

@app.route('/' , methods = ['GET' , 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email=form.email.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password = form.password.data):
            login_user(attempted_user)
            flash(f'Success ! You Are logged in as:{attempted_user.username} ')
            return redirect(url_for('home_page'))
        else:
            print('Đăng nhập thất bại. Tên người dùng và mật khẩu không khớp.')
            flash('Username and password are not match! Please try again')
    
    return render_template('login.html' , form = form)



@app.route('/register' , methods = ['GET' , 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Địa chỉ email đã tồn tại. Vui lòng chọn một địa chỉ email khác.', 'error')
        else:
            user_to_create = User(username=form.username.data, 
                                email=form.email.data, 
                                password=form.password.data)
            db.session.add(user_to_create)
            db.session.commit()
            login_user(user_to_create)
            message = Message(content_user=None, content_chatbot=None,user_id=user_to_create.id)
            db.session.add(message)
            db.session.commit()
            return redirect(url_for('home_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There are an error with creating a user : {err_msg}')
    flash_messages = get_flashed_messages()
    return render_template('register.html' , form = form)
    


@app.route('/chat' , methods = ['GET' , 'POST'])
@login_required
def home_page():
    user = current_user
    messages = user.messages
    if request.method == 'POST':
        text = request.form.get('text')
        chat = chat_predict(text)
        user_id = current_user.id
        message = Message.query.filter_by(user_id=user_id).first()
        if message.content_user is None:
            message.content_user = text
        else:
            message.content_user += '/'+ text
            
        if message.content_chatbot is None:
            message.content_chatbot = chat
        else:
            message.content_chatbot += '/'+ chat
        
        db.session.commit()
       

        return f"{text}|{chat}"

    return render_template('chatbot.html' ,  user=user  ,  messages=messages)

@app.route('/logout')

def logout_page():
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for('login_page'))

@app.route('/clean_messages', methods=['POST'])
def clean_messages():
    user_id = current_user.id
    message = Message.query.filter_by(user_id=user_id).first()

    # Xóa nội dung tin nhắn
    if message:
        message.content_user = None
        message.content_chatbot = None
        db.session.commit()

    return redirect(url_for('home_page'))
    





    
    

