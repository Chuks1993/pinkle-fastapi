from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import BOOLEAN, TIMESTAMP
from app.db.database import Base


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(BOOLEAN, server_default="False", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=True, server_onupdate=text("now()")
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User")


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )


# TODO: Maybe this should be relational
class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, nullable=False, primary_key=True)
    content = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=True, server_onupdate=text("now()")
    )
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
