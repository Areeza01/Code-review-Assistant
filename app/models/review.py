from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from app.database.base import Base

class Review(Base):

    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String)

    language = Column(String)

    issues_found = Column(Integer)

    review_report = Column(Text)
