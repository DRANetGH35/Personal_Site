from flask_login import UserMixin
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from extensions import db

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))
    email: Mapped[str] = mapped_column(String(1000), unique=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False)
    verified: Mapped[bool] = mapped_column(Boolean, nullable=False)
    verification_code: Mapped[str] = mapped_column(String(1000))
