from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from ..db.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    join_date = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
