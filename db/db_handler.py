from datetime import datetime

from sqlalchemy import create_engine, ForeignKey, or_
from sqlalchemy import Column, String, MetaData, Integer, Text, BigInteger, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from constant.message import ReadyMessage
from db.db_config import DatabaseConfig
from balebot.utils.logger import Logger

my_logger = Logger.get_logger()

db_string = DatabaseConfig.db_string
db = create_engine(db_string)
meta = MetaData(db)
Base = declarative_base()
Session = sessionmaker(db)
session = Session()


def create_all_table():
    Base.metadata.create_all(db)
    return True


class Type(Base):
    __tablename__ = 'type'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    category = relationship("Category", cascade="all,delete")

    def __init__(self, name):
        self.name = name


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    type_id = Column(Integer, ForeignKey('type.id', onupdate="CASCADE", ondelete="CASCADE"))
    content_to_category = relationship("ContentToCategory", cascade='all,delete')

    def __init__(self, name, type_id):
        self.name = name
        self.type_id = type_id


class ContentToCategory(Base):
    __tablename__ = 'content_to_category'
    content_id = Column(Integer, ForeignKey('content.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    content = relationship("Content", cascade='all,delete')
    category = relationship("Category", cascade='all,delete')

    def __init__(self, content_id, category_id):
        self.content_id = content_id
        self.category_id = category_id


class Content(Base):
    __tablename__ = 'content'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    nick_name = Column(String, nullable=False)
    content_to_category = relationship("ContentToCategory", cascade='all,delete')
    logo_id = Column(Integer, ForeignKey('logo.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    logo = relationship("Logo", cascade="all,delete", backref="content")
    create_date = Column(DateTime, default=datetime.now())
    allow_publish = Column(Integer, default=0, nullable=False)
    is_sent = Column(Integer, default=0, nullable=False)
    publish_date = Column(DateTime)
    user_id = Column(Integer, nullable=False)
    access_hash = Column(String, nullable=False)

    def __init__(self, name, description, nick_name, logo_id, user_id, access_hash, publish_date):
        self.name = name
        self.description = description
        self.nick_name = nick_name
        self.logo_id = logo_id
        self.user_id = user_id
        self.access_hash = access_hash
        self.publish_date = publish_date

    def __repr__(self):
        return "<Content(name='%s',description='%s',nick_name='%s'" \
               ",content_to_category='%s',logo_id='%s',user_id='%i',access_hash='%s',publish_date='%s)>" % (
                   self.name, self.description, self.nick_name, self.content_to_category,
                   self.logo_id, self.user_id, self.access_hash, self.publish_date)


class Logo(Base):
    __tablename__ = 'logo'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    file_id = Column(BigInteger, nullable=False)
    access_hash = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    thumb = Column(String)
    def __init__(self, file_id, access_hash, file_size, thumb):
        self.file_id = file_id
        self.access_hash = access_hash
        self.file_size = file_size
        self.thumb = thumb


def change_publish_status(content_id, status_code):
    content = session.query(Content).filter(Content.id == content_id).one_or_none()
    try:
        content.allow_publish = status_code
        session.commit()
        return True
    except ValueError:
        print(ValueError)
        return False


def change_text_content(content_id, name=None, nick_name=None, description=None):
    content = session.query(Content).filter(Content.id == int(content_id)).one_or_none()
    try:
        if name:
            content.name = name
        if nick_name:
            content.nick_name = nick_name
        if description:
            content.description = description
        session.commit()
        return True
    except ValueError:
        print(ValueError)
        return False


def change_category_content(content_id, category_id):
    content_to_category = session.query(ContentToCategory).filter(ContentToCategory.content_id == content_id).first()
    try:
        if content_to_category:
            content_to_category.category_id = category_id
        session.commit()
        return True
    except ValueError:
        print(ValueError)
        return False


def change_logo(content_id, logo_id):
    content = session.query(Content).filter(Content.id == content_id).one_or_none()
    try:
        content.logo_id = logo_id
        session.commit()
        return True
    except ValueError:
        print(ValueError)
        return False


def change_is_sent(content_id, is_sent):
    content = session.query(Content).filter(Content.id == content_id).one_or_none()
    try:
        content.is_sent = int(is_sent)
        session.commit()
        return True
    except ValueError:
        print(ValueError)
        return False


def change_type(type_id, new_type_name):
    exact_type = session.query(Type).filter(Type.id == type_id).one_or_none()
    try:
        exact_type.name = new_type_name
        session.commit()
        return True
    except ValueError:
        print(ValueError)
        return False


def change_category(category_id, new_cat_name=None, new_type_id=None):
    category = session.query(Category).filter(Category.id == category_id).one_or_none()
    try:
        if new_cat_name:
            category.name = new_cat_name
        if new_type_id:
            category.type_id = new_type_id
        session.commit()
        return True
    except ValueError:
        print(ValueError)
        return False



def get_accept_content():
    return session.query(Content).filter(Content.is_sent == 0).filter(Content.allow_publish == 1).order_by(
        Content.create_date).all()


def insert_content(content):
    try:
        session.add(content)
        session.commit()
        return content.id
    except ValueError:
        return False
