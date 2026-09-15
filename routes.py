from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
import os, random
from PIL import Image
import base64
import requests
from sqlalchemy import select
from decorators import admin_required
from Cloudinary import list_images
from datetime import datetime
from extensions import db, send_verification_email
from models import User, Comment
from app import create_app
from werkzeug.security import check_password_hash, generate_password_hash

def user_exists(username):
    try:
        if db.session.execute(db.select(User).where(User.name == username)).scalar():
            return True
    except AttributeError:
        return False
    return False

def password_correct(username, password):
    user = db.session.execute(db.select(User).where(User.name == username)).scalar()
    return check_password_hash(user.password, password)

app = create_app()
@app.route('/')
def index():
    return render_template('index.html', current_user=current_user)

@app.route('/travelca')
def travelca():
    comments = db.session.execute(select(Comment)).scalars().all()
    return render_template('travel/ca.html', comments=comments)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if not user_exists(username) or not password_correct(username, password):
            error = "username or password is incorrect"
        else:
            user = db.session.execute(db.select(User).where(User.name == username)).scalar()
            login_user(user)
            return redirect(url_for('index'))
        return render_template('login.html', error=error)
    else: # request method GET
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        entered_password = request.form.get('password')
        password_confirmation = request.form.get('confirm_password')
        verification_code = f"{random.randint(0, 99999):05}"
        if entered_password != password_confirmation:
            error = 'Passwords do not match'
        elif user_exists(username):
            error = 'account with this username already exists'
        else:
            send_verification_email(verification_code, email)
            db.session.add(User(name=username, password=generate_password_hash(entered_password, method="pbkdf2:sha256", salt_length=8), is_admin=False, email=email, verification_code=verification_code, verified=False))
            db.session.commit()
        return render_template('register.html', error=error)
    else: # request method GET
        return render_template('register.html')

@login_required
@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        verification_code = str(request.form.get('verification_code'))
        if request.form.get("verification_code") == current_user.verification_code:
            current_user.verified = True
            db.session.commit()

            return render_template('index.html', current_user=current_user)
        error = "incorrect code"
        return redirect(url_for('verify.html', error=error))
    return render_template('verify.html')

@login_required
@app.route('/comment', methods=['POST'])
def comment():
    text = request.form.get('text')
    today = datetime.today()
    new_comment = Comment(created=today, user=current_user, text=text)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(request.referrer)

@admin_required
@app.route('/delete_comment/<int:comment_id>')
def delete_comment(comment_id):
    comment = db.session.execute(select(Comment).where(Comment.id == comment_id)).scalar()
    db.session.delete(comment)
    db.session.commit()
    return redirect(request.referrer)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile/<username>')
def profile(username):
    user = db.session.execute(db.select(User).where(User.name == username)).scalar()
    return render_template('profile.html')

@app.route('/aboutme')
def aboutme():
    return render_template('aboutme.html')

'''
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        message = f"""Email address: {email}, Message: 
{message}"""
        send_email('devanaptaker@gmail.com', subject, message)
        send_email(email, "Your message has been sent!", "Thanks for contacting dradigital, your message has been sent.")
        return render_template('message_sent.html')
    return render_template('contact.html')
'''

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/Marley_Gallery')
def marley_gallery():
    image_list = list_images()
    return render_template('marley_gallery.html', image_list=image_list)

@app.route('/test')
def test():
    return redirect(request.referrer)

@app.route('/test2')
def test2():
    print(list_images())
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")