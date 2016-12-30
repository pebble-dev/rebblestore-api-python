import enum
import uuid

from flask import g
import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import configure_mappers, sessionmaker, validates
from sqlalchemy.types import CHAR, DateTime, Enum, TypeDecorator
from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils.types import TSVectorType

Column = sqlalchemy.Column
Integer = sqlalchemy.Integer
String = sqlalchemy.String

TableBase = declarative_base()
make_searchable()


class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses Postgresql's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return '%.32x' % uuid.UUID(value).int
            else:
                # hexstring
                return '%.32x' % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)


class PebbleCategory(enum.Enum):
    faces = 'Faces'
    tools = 'Tools & Utilities'
    daily = 'Daily'
    games = 'Games'
    health = 'Health & Fitness'
    remotes = 'Remotes'
    notifications = 'Notifications'
    index = 'Index'
    getsomeapps = 'GetSomeApps'

    @classmethod
    def get_by_value(cls, value):
        for k, v in cls._member_map_.items():
            if v.value == value:
                return getattr(cls, k)
        raise KeyError


class Application(TableBase):
    # TODO: Currently ignoring but should maybe handle:
    # capabilities, changelog, compatibility, images, links?,
    # screenshots, companion apps
    __tablename__ = 'application'

    id = Column(Integer, primary_key=True)
    guid = Column(GUID)
    author = Column(String(length=120))
    title = Column(String(length=256))
    description = Column(String)
    source = Column(String(length=256))
    category = Column(Enum(PebbleCategory))
    create_ts = Column(DateTime)
    publish_ts = Column(DateTime)
    search_vector = Column(TSVectorType('author', 'title', 'description'))

    @validates('author', 'title', 'source')
    def validate_code(self, key, value):
        max_len = getattr(self.__class__, key).prop.columns[0].type.length
        if value and len(value) > max_len:
            return value[:max_len]
        return value

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            # TODO: category id for frontend -_-
            'category': self.category.value,
            'description': self.description,
            # TODO: flesh these out
            'hearts': 0,
            'companions': {
                'android': None,
                'ios': None
            },
            'list_image': {
                '80x80': '',
                '144x144': ''
            },
            'screenshot_hardware': 'basalt',
            'screenshot_images': [
                {'0x0': ''}
            ],
            'icon_image': {
                '28x28': '',
                '48x48': ''
            },
            'capabilities': []
        }


def get_connection():
    db = sqlalchemy.create_engine(
        'postgresql://pebble:pebble@localhost/pebble_app', echo=False)
    configure_mappers()
    Session = sessionmaker(bind=db)
    session = Session()
    return session, db


def get_db():
    """get the connection to the db, but cache it on the g object"""
    if not hasattr(g, 'db'):
        g.db = get_connection()
    return g.db[0], g.db[1]
