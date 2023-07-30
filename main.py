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
    # TODO type_session_id =
    date = Column(TIMESTAMP, nullable=False)


class Coordinates(BaseModel):
    __tablename__ = 'coordinates'

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float, default=0)


class Extent(BaseModel):
    __tablename__ = 'extent'

    # TODO top_left =
    # TODO bot_left =
    # TODO top_right =
    # TODO bot_right =
    pass


class File(BaseModel):
    __tablename__ = 'file'

    name = Column(String, nullable=False)
    path_to_file = Column(String, nullable=False)
    file_extension = Column(String)
    # TODO session_id =


class RawRLI(BaseModel):
    __tablename__ = 'raw_rli'

    # TODO file_id =
    # TODO type_source_rli_id =
    date_receipt = Column(TIMESTAMP, nullable=False)


class RLI(BaseModel):
    __tablename__ = 'rli'

    time_location = Column(TIMESTAMP)
    name = Column(String, nullable=False)
    is_processing = Column(Boolean, nullable=False, default=False)
    # TODO raw_rli_id =


class RasterRLI(BaseModel):
    __tablename__ = 'raster_rli'

    # TODO rli_id =
    # TODO file_id =
    # TODO extent_id =
    pass


class TypeBindingMethod(BaseModel):
    __tablename__ = 'type_binding_method'

    name = Column(String, nullable=False)


class LinkedRLI(BaseModel):
    __tablename__ = 'linked_rli'

    # TODO raster_rli_id =
    # TODO file_id =
    # TODO extent_id =
    binding_attempt_number = Column(Integer)
    # TODO type_binding_method_id =


class Mark(BaseModel):
    __tablename__ = 'mark'

    # TODO coordinates_id =
    datetime = Column(TIMESTAMP, nullable=False)
    # TODO session_id =


class RelatingObject(BaseModel):
    __tablename__ = 'relating_object'

    type_relating = Column(Integer, nullable=False)
    name = Column(String, nullable=False)


class Object(BaseModel):
    __tablename__ = 'object'

    # TODO mark_id =
    name = Column(String)
    type = Column(String)
    # TODO relating_object_id =
    meta = Column(JSON)


class Target(BaseModel):
    __tablename__ = 'target'

    number = Column(Integer, nullable=False)
    # TODO object_id =
    # TODO raster_rli_id =
    datetime_sending = Column(TIMESTAMP)
    sppr_type_key = Column(String)


class Region(BaseModel):
    __tablename__ = 'region'

    # TODO extent_id =
    name = Column(String)





# Создание таблиц
Base.metadata.create_all(bind=engine)

