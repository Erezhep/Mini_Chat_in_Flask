from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_manager, login_required, UserMixin, LoginManager, login_user, current_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = "@#rrfer23$F43etgv$%#tgb54eTFGVbt543WTgbtr543wtgerv"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///blog_db_flask.db'
db = SQLAlchemy(app)


class UserInfo(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable = True)
    password = db.Column(db.String(300), nullable = False)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1023), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return UserInfo.query.get(int(user_id))


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = UserInfo.query.filter_by(username=username).first()

        if username == "" or password == "":
            flash("Заполните все поля", category="login-field")

        if user is None:
            flash("Нет такого пользователя", category='login-user')
        elif not check_password_hash(user.password, password):
            flash("Неверный пароль", category='login-password')
        else:
            login_user(user)
            return redirect(url_for('chat'))

    return render_template("login.html")


def is_username_unique(username):
    return UserInfo.query.filter_by(username=username).first() is None

# Функция для обработки страницы регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if username == "" or password == "" or confirm_password == "":
            flash("Заполните все поля", category="register-field")

        if not is_username_unique(username):
            flash("Такой пользователь уже существует", category="register-user")

        if password != confirm_password:
            flash("Пароли не совпадают", category="register-password")
        else:
            hashed_password = generate_password_hash(password)
            new_user = UserInfo(username=username, password=hashed_password)

            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('chat'))

    return render_template('login.html')


@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/ajax_messages', methods = ['GET', 'POST'])
# @login_required
def ajax_request():
    if request.method == "POST":
        if request.is_json:  # Убедитесь, что запрос содержит JSON
            data = request.json
            new_message = Article(text=data['message'], user_id=current_user.id)
            db.session.add(new_message)
            db.session.commit()
            return jsonify(status='success'), 200

    messages = Article.query.order_by(Article.created_at).limit(100).all()
    formatted_messages = []

    formatted_messages.append({"user_real_time": current_user.username, 'id_user_real_time': current_user.id})    

    for message in messages:
        user_info = UserInfo.query.get(message.user_id)
        formatted_message = {
            'message': message.text,
            'user_id': message.user_id,
            'created_at': message.created_at.strftime('%H:%M'),
            'user_name': user_info.username
        }
        formatted_messages.append(formatted_message)

    return jsonify(messages=formatted_messages), 200  

if __name__ == '__main__':
    app.run(
        debug=True,
        port=2025)