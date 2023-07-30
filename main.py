from sqlalchemy import create_engine, Boolean, JSON, TIMESTAMP, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Создание подключения к базе данных
engine = create_engine('sqlite:///RLSDB.db')

SessionDB = sessionmaker(bind=engine)
session = SessionDB()

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class TypeSession(BaseModel):
    __tablename__ = 'type_session'

    name = Column(String, nullable=False)


class TypeSourceRLI(BaseModel):
    __tablename__ = 'type_source_rli'

    name = Column(String, nullable=False)


class Session(BaseModel):
    __tablename__ = 'session'

    name = Column(String, nullable=False)
    path_to_directory = Column(String, nullable=False)
    type_session_id = Column(Integer, ForeignKey('type_session.id', ondelete='CASCADE'))
    date = Column(TIMESTAMP, nullable=False)


class Coordinates(BaseModel):
    __tablename__ = 'coordinates'

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float, default=0)


class Extent(BaseModel):
    __tablename__ = 'extent'

    top_left = Column(Integer, ForeignKey('coordinates.id', ondelete='CASCADE'))
    bot_left = Column(Integer, ForeignKey('coordinates.id', ondelete='CASCADE'))
    top_right = Column(Integer, ForeignKey('coordinates.id', ondelete='CASCADE'))
    bot_right = Column(Integer, ForeignKey('coordinates.id', ondelete='CASCADE'))


class File(BaseModel):
    __tablename__ = 'file'

    name = Column(String, nullable=False)
    path_to_file = Column(String, nullable=False)
    file_extension = Column(String)
    session_id = Column(Integer, ForeignKey('session.id', ondelete='CASCADE'))


class RawRLI(BaseModel):
    __tablename__ = 'raw_rli'

    file_id = Column(Integer, ForeignKey('file.id', ondelete='CASCADE'))
    type_source_rli_id = Column(Integer, ForeignKey('type_source_rli.id', ondelete='CASCADE'))
    date_receiving = Column(TIMESTAMP, nullable=False)


class RLI(BaseModel):
    __tablename__ = 'rli'

    time_location = Column(TIMESTAMP)
    name = Column(String, nullable=False)
    is_processing = Column(Boolean, nullable=False, default=False)
    raw_rli_id = Column(Integer, ForeignKey('raw_rli.id', ondelete='CASCADE'))


class RasterRLI(BaseModel):
    __tablename__ = 'raster_rli'

    rli_id = Column(Integer, ForeignKey('rli.id', ondelete='CASCADE'))
    file_id = Column(Integer, ForeignKey('file.id', ondelete='CASCADE'))
    extent_id = Column(Integer, ForeignKey('extent.id', ondelete='CASCADE'))


class TypeBindingMethod(BaseModel):
    __tablename__ = 'type_binding_method'

    name = Column(String, nullable=False)


class LinkedRLI(BaseModel):
    __tablename__ = 'linked_rli'

    raster_rli_id = Column(Integer, ForeignKey('raster_rli.id', ondelete='CASCADE'))
    file_id = Column(Integer, ForeignKey('file.id', ondelete='CASCADE'))
    extent_id = Column(Integer, ForeignKey('extent.id', ondelete='CASCADE'))
    binding_attempt_number = Column(Integer)
    type_binding_method_id = Column(Integer, ForeignKey('type_binding_method.id', ondelete='CASCADE'))


class Mark(BaseModel):
    __tablename__ = 'mark'

    coordinates_id = Column(Integer, ForeignKey('coordinates.id', ondelete='CASCADE'))
    datetime = Column(TIMESTAMP, nullable=False)
    session_id = Column(Integer, ForeignKey('session.id', ondelete='CASCADE'))


class RelatingObject(BaseModel):
    __tablename__ = 'relating_object'

    type_relating = Column(Integer, nullable=False)
    name = Column(String, nullable=False)


class Object(BaseModel):
    __tablename__ = 'object'

    mark_id = Column(Integer, ForeignKey('mark.id', ondelete='CASCADE'))
    name = Column(String)
    type = Column(String)
    relating_object_id = Column(Integer, ForeignKey('relating_object.id', ondelete='CASCADE'))
    meta = Column(JSON)


class Target(BaseModel):
    __tablename__ = 'target'

    number = Column(Integer, nullable=False)
    object_id = Column(Integer, ForeignKey('object.id', ondelete='CASCADE'))
    raster_rli_id = Column(Integer, ForeignKey('raster_rli.id', ondelete='CASCADE'))
    datetime_sending = Column(TIMESTAMP)
    sppr_type_key = Column(String)


class Region(BaseModel):
    __tablename__ = 'region'

    extent_id = Column(Integer, ForeignKey('extent.id', ondelete='CASCADE'))
    name = Column(String)





# Создание таблиц
Base.metadata.create_all(bind=engine)

