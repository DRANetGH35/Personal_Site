from flask import Flask
from flask_migrate import Migrate
from datetime import timedelta
from sqlalchemy import select
from extensions import db, login_manager, bootstrap
from models import User


def create_app():
    app = Flask(__name__)

    with open('csrfkey.txt', 'r') as file:
        app.config['SECRET_KEY'] = file.readline().strip('\n')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site_database.db'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Time the user out after 30 minutes
    app.config['SERVER_NAME'] = 'dradigital.net'
    app.config['PERFERRED_URL_SCHEME'] = 'https'
    app.config['APPLICATION_ROOT']= '/'
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['REMEMBER_COOKIE_SECURE'] = True

    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    migrate = Migrate(app, db)

    @login_manager.user_loader
    def load_user(user_id):
        user_to_load = db.session.execute(select(User).where(User.id == user_id)).scalar()
        if user_to_load:
            return user_to_load
        else:
            return None


    #with app.app_context():
    #    db.create_all()



    return app