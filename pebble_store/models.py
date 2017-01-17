import uuid

import arrow
from flask import g
import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (configure_mappers, relationship,
                            scoped_session, sessionmaker, validates)
from sqlalchemy.types import Boolean, CHAR, TypeDecorator
from sqlalchemy.schema import ForeignKey
from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils.types import ArrowType, ChoiceType, TSVectorType

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


ApplicationCollection = sqlalchemy.Table('application_tag', TableBase.metadata,
                                         Column('collection_id',
                                                ForeignKey('collection.id')),
                                         Column('application_id',
                                                ForeignKey('application.id')))


class Collection(TableBase):
    __tablename__ = 'collection'
    __tableargs__ = (
        sqlalchemy.UniqueConstraint('name', 'type')
    )

    TYPES = [
        ('tag', 'Tag'),
        ('category', 'Category')
    ]

    id = Column(Integer, primary_key=True)
    type = Column(ChoiceType(TYPES))
    name = Column(String(length=50))
    featured = Column(Boolean, default=False)
    create_ts = Column(ArrowType, default=arrow.utcnow)
    modify_ts = Column(ArrowType, default=arrow.utcnow)
    applications = relationship('Application', secondary=ApplicationCollection,
                                back_populates='collections')


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
    hearts = Column(Integer, default=0)
    source = Column(String(length=256))
    create_ts = Column(ArrowType, default=arrow.utcnow)
    publish_ts = Column(ArrowType, default=arrow.utcnow)
    search_vector = Column(TSVectorType('author', 'title', 'description'))

    collections = relationship('Collection', secondary=ApplicationCollection,
                               back_populates='applications')
    files = relationship('File', back_populates='application')

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
            'description': self.description,
            # TODO: flesh these out
            'hearts': self.hearts,
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


class File(TableBase):
    __tablename__ = 'file'
    TYPES = [
        ('header', 'header'),
        ('icon', 'icon'),
        ('list', 'list'),
        ('screenshot', 'screenshot'),
        ('pbw', 'pbw'),
    ]

    id = Column(Integer, primary_key=True)
    sha256 = Column(String(length=64), unique=True)
    application_id = Column(Integer, ForeignKey('application.id'),
                            nullable=False)
    type = Column(ChoiceType(TYPES))
    path = Column(String)
    image_width = Column(Integer, default=0)
    image_height = Column(Integer, default=0)

    application = relationship('Application', back_populates='files')


def get_connection(host, db, user, password):
    db = sqlalchemy.create_engine(
        'postgresql://{user}:{password}@{host}/{db}'.format(
            user=user, password=password, host=host, db=db),
        echo=False)
    configure_mappers()
    Session = scoped_session(sessionmaker(bind=db))
    return Session, db


def get_db():
    """get the connection to the db, but cache it on the g object"""
    if not hasattr(g, 'db'):
        host = current_app.config.get('DB_HOST', 'localhost')
        db = current_app.config.get('DB_DB', 'rebble')
        user = current_app.config.get('DB_USER', 'rebble')
        password = current_app.config.get('DB_PASSWORD', 'rebble')
        g.db = get_connection(host, db, user, password)

    return g.db[0], g.db[1]
