from flask import render_template
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