from flask import render_template, request, redirect
from flask_login import current_user
from extensions import db
from models import User
from app import create_app
from werkzeug.security import check_password_hash, generate_password_hash

def user_exists(username):
    try:
        if db.session.execute(db.select(User).where(User.name == username)).scalar():
            return True
    except AttributeError:
        return False

app = create_app()
@app.route('/')
def index():
    logged_in = False
    if current_user.is_authenticated:
        logged_in = True
    return render_template('index.html', logged_in=logged_in)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    error=''
    if request.method == "POST":
        username = request.form.get('username')
        entered_password = request.form.get('password')
        password_confirmation = request.form.get('confirm_password')
        print(username, entered_password, password_confirmation)
        if entered_password != password_confirmation:
            error = 'Passwords do not match'
        elif user_exists(username):
            error = 'account with this username already exists'
        else:
            db.session.add(User(name=username, password=generate_password_hash(entered_password, method="pbkdf2:sha256", salt_length=8), is_admin=False))
            db.session.commit()
        return render_template('register.html', error=error)
    elif request.method == 'GET':
        return render_template('register.html')
