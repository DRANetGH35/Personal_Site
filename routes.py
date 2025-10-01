from flask import render_template, request, redirect
from flask_login import current_user
from extensions import db
from models import User
from app import create_app

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
    if request.method == "POST":
        entered_password = request.form.get('password')
        password_confirmation = request.form.get('confirm_password')
        if entered_password == password_confirmation:
            #enter user info into database
            pass
        else:
            print('passwords dont match')
        return render_template('register.html')
    else:
        return render_template('register.html')
