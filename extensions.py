from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from sqlalchemy.orm import DeclarativeBase
import os

emailpsswd = os.environ.get('emailpsswd')

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
bootstrap = Bootstrap5()
