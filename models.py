from flask_login import UserMixin
from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
import datetime

from extensions import db

class User(UserMixin, db.Model):
    __table_name__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))
    email: Mapped[str] = mapped_column(String(1000), unique=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False)
    verified: Mapped[bool] = mapped_column(Boolean, nullable=False)
    verification_code: Mapped[str] = mapped_column(String(1000))
    comments: Mapped[List["Comment"]] = relationship(back_populates="user")

class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime)
    text: Mapped[str] = mapped_column(String(1000))
    user: Mapped[User] = relationship("User", back_populates="comments")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))