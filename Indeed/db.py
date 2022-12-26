from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Ads(Base):
    __tablename__ = "ads"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    company = Column(String)
    description = Column(String)
    link = Column(String)


def get_engine():
    return create_engine(f"sqlite:///indeed.db")


def get_session(engine):
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    return session


def create_table(engine):
    Base.metadata.create_all(engine, checkfirst=True)
