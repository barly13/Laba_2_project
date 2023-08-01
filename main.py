from sqlalchemy import create_engine, Boolean, JSON, TIMESTAMP, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import threading
from datetime import datetime

# Создание подключения к базе данных
engine = create_engine('sqlite:///RLSDB.db')

SessionDB = sessionmaker(bind=engine)
session = SessionDB()

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)

    mutex = threading.Lock()

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class TypeSession(BaseModel):
    __tablename__ = 'type_session'

    name = Column(String, nullable=False)

    # Функция для создания объекта TypeSession
    @classmethod
    def create_type_session(cls, name):
        with cls.mutex:
            new_type_session = cls(name=name)
            session.add(new_type_session)
            session.commit()

    # Функция для удаления объекта TypeSession по id
    @classmethod
    def delete_type_session(cls, type_session_id):
        with cls.mutex:
            type_session = session.query(cls).get(type_session_id)
            if type_session:
                session.delete(type_session)
                session.commit()

    # Функция для изменения объекта TypeSession по id
    @classmethod
    def update_type_session(cls, type_session_id, new_name):
        with cls.mutex:
            type_session = session.query(cls).get(type_session_id)
            if type_session:
                type_session.name = new_name
                session.commit()


class TypeSourceRLI(BaseModel):
    __tablename__ = 'type_source_rli'

    name = Column(String, nullable=False)

    # Функция для создания объекта TypeSourceRLI
    @classmethod
    def create_type_source_rli(cls, name):
        with cls.mutex:
            new_type_source_rli = cls(name=name)
            session.add(new_type_source_rli)
            session.commit()

    # Функция для удаления объекта TypeSourceRLI по id
    @classmethod
    def delete_type_source_rli(cls, type_source_rli_id):
        with cls.mutex:
            type_source_rli = session.query(cls).get(type_source_rli_id)
            if type_source_rli:
                session.delete(type_source_rli)
                session.commit()

    # Функция для изменения объекта TypeSourceRLI по id
    @classmethod
    def update_type_source_rli(cls, type_source_rli_id, new_name):
        with cls.mutex:
            type_source_rli = session.query(cls).get(type_source_rli_id)
            if type_source_rli:
                type_source_rli.name = new_name
                session.commit()


class Session(BaseModel):
    __tablename__ = 'session'

    name = Column(String, nullable=False)
    path_to_directory = Column(String, nullable=False)
    type_session_id = Column(Integer, ForeignKey('type_session.id', ondelete='CASCADE'))
    date = Column(TIMESTAMP, nullable=False)

    # Функция для создания объекта Session
    @classmethod
    def create_session(cls, name, path_to_directory, type_session_id):
        with cls.mutex:
            new_session = cls(name=name, path_to_directory=path_to_directory,
                              type_session_id=type_session_id, date=datetime.now())
            session.add(new_session)
            session.commit()

    # Функция для удаления объекта Session по id
    @classmethod
    def delete_session(cls, session_id):
        with cls.mutex:
            session_obj = session.query(cls).get(session_id)
            if session_obj:
                session.delete(session_obj)
                session.commit()

    # Функция для изменения объекта Session по id
    @classmethod
    def update_session(cls, session_id, new_name, new_path_to_directory, new_type_session_id):
        with cls.mutex:
            session_obj = session.query(cls).get(session_id)
            if session_obj:
                session_obj.name = new_name
                session_obj.path_to_directory = new_path_to_directory
                session_obj.type_session_id = new_type_session_id
                session_obj.date = datetime.now()
                session.commit()


class Coordinates(BaseModel):
    __tablename__ = 'coordinates'

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float, default=0)

    # Функция для создания объекта Coordinates
    @classmethod
    def create_coordinates(cls, latitude, longitude, altitude):
        with cls.mutex:
            new_coordinates = cls(latitude=latitude, longitude=longitude, altitude=altitude)
            session.add(new_coordinates)
            session.commit()

    # Функция для удаления объекта Coordinates по id
    @classmethod
    def delete_coordinates(cls, coordinates_id):
        with cls.mutex:
            coordinates = session.query(cls).get(coordinates_id)
            if coordinates:
                session.delete(coordinates)
                session.commit()

    # Функция для изменения объекта Coordinates по id
    @classmethod
    def update_coordinates(cls, coordinates_id, new_latitude, new_longitude, new_altitude):
        with cls.mutex:
            coordinates = session.query(cls).get(coordinates_id)
            if coordinates:
                coordinates.latitude = new_latitude
                coordinates.longitude = new_longitude
                coordinates.altitude = new_altitude
                session.commit()


class Extent(BaseModel):
    __tablename__ = 'extent'

    top_left = Column(Integer, ForeignKey('coordinates.id', ondelete='CASCADE'))
    bot_left = Column(Integer, ForeignKey('coordinates.id', ondelete='CASCADE'))
    top_right = Column(Integer, ForeignKey('coordinates.id', ondelete='CASCADE'))
    bot_right = Column(Integer, ForeignKey('coordinates.id', ondelete='CASCADE'))

    # Функция для создания объекта Extent
    @classmethod
    def create_extent(cls, top_left, bot_left, top_right, bot_right):
        with cls.mutex:
            new_extent = cls(top_left=top_left, bot_left=bot_left, top_right=top_right, bot_right=bot_right)
            session.add(new_extent)
            session.commit()

    # Функция для удаления объекта Extent по id
    @classmethod
    def delete_extent(cls, extent_id):
        with cls.mutex:
            extent = session.query(cls).get(extent_id)
            if extent:
                session.delete(extent)
                session.commit()

    # Функция для изменения объекта Extent по id
    @classmethod
    def update_extent(cls, extent_id, new_top_left, new_bot_left, new_top_right, new_bot_right):
        with cls.mutex:
            extent = session.query(cls).get(extent_id)
            if extent:
                extent.top_left = new_top_left
                extent.bot_left = new_bot_left
                extent.top_right = new_top_right
                extent.bot_right = new_bot_right
                session.commit()


class File(BaseModel):
    __tablename__ = 'file'

    name = Column(String, nullable=False)
    path_to_file = Column(String, nullable=False)
    file_extension = Column(String)
    session_id = Column(Integer, ForeignKey('session.id', ondelete='CASCADE'))

    # Функция для создания объекта File
    @classmethod
    def create_file(cls, name, path_to_file, file_extension, session_id):
        with cls.mutex:
            new_file = cls(name=name, path_to_file=path_to_file, file_extension=file_extension, session_id=session_id)
            session.add(new_file)
            session.commit()

    # Функция для удаления объекта File по id
    @classmethod
    def delete_file(cls, file_id):
        with cls.mutex:
            file = session.query(cls).get(file_id)
            if file:
                session.delete(file)
                session.commit()

    # Функция для изменения объекта File по id
    @classmethod
    def update_file(cls, file_id, new_name, new_path_to_file, new_file_extension, new_session_id):
        with cls.mutex:
            file = session.query(cls).get(file_id)
            if file:
                file.name = new_name
                file.path_to_file = new_path_to_file
                file.file_extension = new_file_extension
                file.session_id = new_session_id
                session.commit()


class RawRLI(BaseModel):
    __tablename__ = 'raw_rli'

    file_id = Column(Integer, ForeignKey('file.id', ondelete='CASCADE'))
    type_source_rli_id = Column(Integer, ForeignKey('type_source_rli.id', ondelete='CASCADE'))
    date_receiving = Column(TIMESTAMP, nullable=False)

    # Функция для создания объекта RawRLI
    @classmethod
    def create_raw_rli(cls, file_id, type_source_rli_id):
        with cls.mutex:
            new_raw_rli = cls(file_id=file_id, type_source_rli_id=type_source_rli_id, date_receiving=datetime.now())
            session.add(new_raw_rli)
            session.commit()

    # Функция для удаления объекта RawRLI по id
    @classmethod
    def delete_raw_rli(cls, raw_rli_id):
        with cls.mutex:
            raw_rli = session.query(cls).get(raw_rli_id)
            if raw_rli:
                session.delete(raw_rli)
                session.commit()

    # Функция для изменения объекта RawRLI по id
    @classmethod
    def update_raw_rli(cls, raw_rli_id, new_file_id, new_type_source_rli_id):
        with cls.mutex:
            raw_rli = session.query(cls).get(raw_rli_id)
            if raw_rli:
                raw_rli.file_id = new_file_id
                raw_rli.type_source_rli_id = new_type_source_rli_id
                raw_rli.date_receiving = datetime.now()
                session.commit()


class RLI(BaseModel):
    __tablename__ = 'rli'

    time_location = Column(TIMESTAMP)
    name = Column(String, nullable=False)
    is_processing = Column(Boolean, nullable=False, default=False)
    raw_rli_id = Column(Integer, ForeignKey('raw_rli.id', ondelete='CASCADE'))

    # Функция для создания объекта RLI
    @classmethod
    def crate_rli(cls, name, is_processing, raw_rli_id):
        with cls.mutex:
            new_rli = cls(time_location=datetime.now(), name=name, is_processing=is_processing, raw_rli_id=raw_rli_id)
            session.add(new_rli)
            session.commit()

    # Функция для удаления объекта RLI по id
    @classmethod
    def delete_rli(cls, rli_id):
        with cls.mutex:
            rli = session.query(cls).get(rli_id)
            if rli:
                session.delete(rli)
                session.commit()

    # Функция для изменения объекта RLI по id
    @classmethod
    def update_rli(cls, rli_id, new_name, new_is_processing, new_raw_rli_id):
        with cls.mutex:
            rli = session.query(cls).get(rli_id)
            if rli:
                rli.time_location = datetime.now()
                rli.name = new_name
                rli.is_processing = new_is_processing
                rli.raw_rli_id = new_raw_rli_id
                session.commit()


class RasterRLI(BaseModel):
    __tablename__ = 'raster_rli'

    rli_id = Column(Integer, ForeignKey('rli.id', ondelete='CASCADE'))
    file_id = Column(Integer, ForeignKey('file.id', ondelete='CASCADE'))
    extent_id = Column(Integer, ForeignKey('extent.id', ondelete='CASCADE'))

    # Функция создания объекта RasterRLI
    @classmethod
    def create_raster_rli(cls, rli_id, file_id, extent_id):
        with cls.mutex:
            new_raster_rli = cls(rli_id=rli_id, file_id=file_id, extent_id=extent_id)
            session.add(new_raster_rli)
            session.commit()

    # Функция для удаления объекта RasterRLI по id
    @classmethod
    def delete_raster_rli(cls, raster_rli_id):
        with cls.mutex:
            raster_rli = session.query(cls).get(raster_rli_id)
            if raster_rli:
                session.delete(raster_rli)
                session.commit()

    # Функция для изменения объекта RasterRLI по id
    @classmethod
    def update_raster_rli(cls, raster_rli_id, new_rli_id, new_file_id, new_extent_id):
        with cls.mutex:
            raster_rli = session.query(cls).get(raster_rli_id)
            if raster_rli:
                raster_rli.rli_id = new_rli_id
                raster_rli.file_id = new_file_id
                raster_rli.extent_id = new_extent_id
                session.commit()


class TypeBindingMethod(BaseModel):
    __tablename__ = 'type_binding_method'

    name = Column(String, nullable=False)

    # Функция для создания объекта TypeBindingMethod
    @classmethod
    def create_type_binding_method(cls, name):
        with cls.mutex:
            new_type_binding_method = cls(name=name)
            session.add(new_type_binding_method)
            session.commit()

    # Функция для удаления объекта TypeBindingMethod по id
    @classmethod
    def delete_type_binding_method(cls, type_binding_method_id):
        with cls.mutex:
            type_binding_method = session.query(cls).get(type_binding_method_id)
            if type_binding_method:
                session.delete(type_binding_method)
                session.commit()

    # Функция для изменения объекта TypeBindingMethod по id
    @classmethod
    def update_type_binding_method(cls, type_binding_method_id, new_name):
        with cls.mutex:
            type_binding_method = session.query(cls).get(type_binding_method_id)
            if type_binding_method:
                type_binding_method.name = new_name
                session.commit()


class LinkedRLI(BaseModel):
    __tablename__ = 'linked_rli'

    raster_rli_id = Column(Integer, ForeignKey('raster_rli.id', ondelete='CASCADE'))
    file_id = Column(Integer, ForeignKey('file.id', ondelete='CASCADE'))
    extent_id = Column(Integer, ForeignKey('extent.id', ondelete='CASCADE'))
    binding_attempt_number = Column(Integer)
    type_binding_method_id = Column(Integer, ForeignKey('type_binding_method.id', ondelete='CASCADE'))

    # Функция для создания объекта LinkedRLI
    @classmethod
    def create_linked_rli(cls, raster_rli_id, file_id, extent_id, binding_attempt_number, type_binding_method_id):
        with cls.mutex:
            new_linked_rli = cls(raster_rli_id=raster_rli_id, file_id=file_id, extent_id=extent_id,
                                 binding_attempt_number=binding_attempt_number,
                                 type_binding_method_id=type_binding_method_id)
            session.add(new_linked_rli)
            session.commit()

    # Функция для удаления объекта LinkedRLI по id
    @classmethod
    def delete_linked_rli(cls, linked_rli_id):
        with cls.mutex:
            linked_rli = session.query(cls).get(linked_rli_id)
            if linked_rli:
                session.delete(linked_rli)
                session.commit()

    # Функция для изменения объекта LinkedRLI по id
    @classmethod
    def update_linked_rli(cls, linked_rli_id, new_raster_rli_id, new_file_id, new_extent_id,
                          new_binding_attempt_number, new_type_binding_method_id):
        with cls.mutex:
            linked_rli = session.query(cls).get(linked_rli_id)
            if linked_rli:
                linked_rli.raster_rli_id = new_raster_rli_id
                linked_rli.file_id = new_file_id
                linked_rli.extent_id = new_extent_id
                linked_rli.binding_attempt_number = new_binding_attempt_number
                linked_rli.type_binding_method_id = new_type_binding_method_id
                session.commit()


class Mark(BaseModel):
    __tablename__ = 'mark'

    coordinates_id = Column(Integer, ForeignKey('coordinates.id', ondelete='CASCADE'))
    datetime = Column(TIMESTAMP, nullable=False)
    session_id = Column(Integer, ForeignKey('session.id', ondelete='CASCADE'))

    # Функция для создания объекта Mark
    @classmethod
    def create_mark(cls, coordinates_id, session_id):
        with cls.mutex:
            new_mark = cls(coordinates_id=coordinates_id, datetime=datetime.now(), session_id=session_id)
            session.add(new_mark)
            session.commit()

    # Функция для удаления объекта Mark по id
    @classmethod
    def delete_mark(cls, mark_id):
        with cls.mutex:
            mark = session.query(cls).get(mark_id)
            if mark:
                session.delete(mark)
                session.commit()

    # Функция для изменения объекта Mark по id
    @classmethod
    def update_mark(cls, mark_id, new_coordinates_id, new_session_id):
        with cls.mutex:
            mark = session.query(cls).get(mark_id)
            if mark:
                mark.coordinates_id = new_coordinates_id
                mark.datetime = datetime.now()
                mark.session_id = new_session_id
                session.commit()


class RelatingObject(BaseModel):
    __tablename__ = 'relating_object'

    type_relating = Column(Integer, nullable=False)
    name = Column(String, nullable=False)

    # Функция для создания объекта RelatingObject
    @classmethod
    def create_relating_object(cls, type_relating, name):
        with cls.mutex:
            new_relating_object = cls(type_relating=type_relating, name=name)
            session.add(new_relating_object)
            session.commit()

    # Функция для удаления объекта RelatingObject по id
    @classmethod
    def delete_relating_object(cls, relating_object_id):
        with cls.mutex:
            relating_object = session.query(cls).get(relating_object_id)
            if relating_object:
                session.delete(relating_object)
                session.commit()

    # Функция для изменения объекта RelatingObject по id
    @classmethod
    def update_relating_object(cls, relating_object_id, new_type_relating, new_name):
        with cls.mutex:
            relating_object = session.query(cls).get(relating_object_id)
            if relating_object:
                relating_object.type_relating = new_type_relating
                relating_object.name = new_name
                session.commit()


class Object(BaseModel):
    __tablename__ = 'object'

    mark_id = Column(Integer, ForeignKey('mark.id', ondelete='CASCADE'))
    name = Column(String)
    object_type = Column(String)
    relating_object_id = Column(Integer, ForeignKey('relating_object.id', ondelete='CASCADE'))
    meta = Column(JSON)

    # Функция для создания объекта Object
    @classmethod
    def create_object(cls, mark_id, name, object_type, relating_object_id, meta):
        with cls.mutex:
            new_object = cls(mark_id=mark_id, name=name, object_type=object_type,
                             relating_object_id=relating_object_id, meta=meta)
            session.add(new_object)
            session.commit()

    # Функция для удаления объекта Object по id
    @classmethod
    def delete_object(cls, object_id):
        with cls.mutex:
            object_ = session.query(cls).get(object_id)
            if object_:
                session.delete(object_)
                session.commit()

    # Функция для изменения объекта Object по id
    @classmethod
    def update_object(cls, object_id, new_mark_id, new_name, new_relating_object_id, new_meta):
        with cls.mutex:
            object_ = session.query(cls).get(object_id)
            if object_:
                object_.mark_id = new_mark_id
                object_.name = new_name
                object_.relating_object_id = new_relating_object_id
                object_.meta = new_meta
                session.commit()


class Target(BaseModel):
    __tablename__ = 'target'

    number = Column(Integer, nullable=False)
    object_id = Column(Integer, ForeignKey('object.id', ondelete='CASCADE'))
    raster_rli_id = Column(Integer, ForeignKey('raster_rli.id', ondelete='CASCADE'))
    datetime_sending = Column(TIMESTAMP)
    sppr_type_key = Column(String)

    # Функция для создания объекта Target
    @classmethod
    def create_target(cls, number, object_id, raster_rli_id, sppr_type_key):
        with cls.mutex:
            new_target = cls(number=number, object_id=object_id, raster_rli_id=raster_rli_id,
                             datetime_sending=datetime.now(), sppr_type_key=sppr_type_key)
            session.add(new_target)
            session.commit()

    # Функция для удаления объекта Target по id
    @classmethod
    def delete_target(cls, target_id):
        with cls.mutex:
            target = session.query(cls).get(target_id)
            if target:
                session.delete(target)
                session.commit()

    # Функция для изменения объекта Target по id
    @classmethod
    def update_target(cls, target_id, new_number, new_object_id, new_raster_rli_id, new_sppr_type_key):
        with cls.mutex:
            target = session.query(cls).get(target_id)
            if target:
                target.number = new_number
                target.object_id = new_object_id
                target.raster_rli_id = new_raster_rli_id
                target.sppr_type_key = new_sppr_type_key
                session.commit()


class Region(BaseModel):
    __tablename__ = 'region'

    extent_id = Column(Integer, ForeignKey('extent.id', ondelete='CASCADE'))
    name = Column(String)

    # Функция для создания объекта Region
    @classmethod
    def create_region(cls, extent_id, name):
        with cls.mutex:
            new_region = cls(extent_id=extent_id, name=name)
            session.add(new_region)
            session.commit()

    # Функция для удаления объекта Region по id
    @classmethod
    def delete_region(cls, region_id):
        with cls.mutex:
            region = session.query(cls).get(region_id)
            if region:
                session.delete(region)
                session.commit()

    # Функция для изменения объекта Region по id
    @classmethod
    def update_region(cls, region_id, new_extent_id, new_name):
        with cls.mutex:
            region = session.query(cls).get(region_id)
            if region:
                region.extent_id = new_extent_id
                region.name = new_name
                session.commit()


# Создание таблиц
Base.metadata.create_all(bind=engine)
