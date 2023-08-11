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


class BaseEntity(Base):
    __abstract__ = True
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)

    mutex = threading.Lock()

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class TypeSessionEntity(BaseEntity):
    __tablename__ = 'type_session'

    name = Column(String, nullable=False)

    # Функция для создания объекта TypeSessionEntity
    @classmethod
    def create_type_session(cls, name):
        with cls.mutex:
            new_type_session = cls(name=name)
            session.add(new_type_session)
            session.commit()
            return new_type_session.id

    # Функция для удаления объекта TypeSessionEntity по id
    @classmethod
    def delete_type_session(cls, type_session_id):
        with cls.mutex:
            type_session = session.query(cls).get(type_session_id)
            if type_session:
                session.delete(type_session)
                session.commit()

    # Функция для изменения объекта TypeSessionEntity по id
    @classmethod
    def update_type_session(cls, type_session_id, new_name):
        with cls.mutex:
            type_session = session.query(cls).get(type_session_id)
            if type_session:
                type_session.name = new_name
                session.commit()


class TypeSourceRLIEntity(BaseEntity):
    __tablename__ = 'type_source_rli'

    name = Column(String, nullable=False)

    # Функция для создания объекта TypeSourceRLIEntity
    @classmethod
    def create_type_source_rli(cls, name):
        with cls.mutex:
            new_type_source_rli = cls(name=name)
            session.add(new_type_source_rli)
            session.commit()
            return new_type_source_rli.id

    # Функция для удаления объекта TypeSourceRLIEntity по id
    @classmethod
    def delete_type_source_rli(cls, type_source_rli_id):
        with cls.mutex:
            type_source_rli = session.query(cls).get(type_source_rli_id)
            if type_source_rli:
                session.delete(type_source_rli)
                session.commit()

    # Функция для изменения объекта TypeSourceRLIEntity по id
    @classmethod
    def update_type_source_rli(cls, type_source_rli_id, new_name):
        with cls.mutex:
            type_source_rli = session.query(cls).get(type_source_rli_id)
            if type_source_rli:
                type_source_rli.name = new_name
                session.commit()


class SessionEntity(BaseEntity):
    __tablename__ = 'session'

    name = Column(String, nullable=False)
    path_to_directory = Column(String, nullable=False)
    type_session_id = Column(Integer, ForeignKey('type_session.id', ondelete='CASCADE'))
    type_session = relationship('TypeSessionEntity')
    date = Column(TIMESTAMP, nullable=False)

    # Функция для создания объекта SessionEntity
    @classmethod
    def create_session(cls, name, path_to_directory, type_session_id):
        with cls.mutex:
            new_session = cls(name=name, path_to_directory=path_to_directory,
                              type_session_id=type_session_id, date=datetime.now())
            session.add(new_session)
            session.commit()
            return new_session.id

    # Функция для удаления объекта SessionEntity по id
    @classmethod
    def delete_session(cls, session_id):
        with cls.mutex:
            session_obj = session.query(cls).get(session_id)
            if session_obj:
                session.delete(session_obj)
                session.commit()

    # Функция для изменения объекта SessionEntity по id
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

    # Функция получения перечня сессий
    @classmethod
    def get_all_sessions(cls):
        with cls.mutex:
            return session.query(cls).all()


class CoordinatesEntity(BaseEntity):
    __tablename__ = 'coordinates'

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float, default=0)

    # Функция для создания объекта CoordinatesEntity
    @classmethod
    def create_coordinates(cls, latitude, longitude, altitude):
        with cls.mutex:
            new_coordinates = cls(latitude=latitude, longitude=longitude, altitude=altitude)
            session.add(new_coordinates)
            session.commit()
            return new_coordinates.id

    # Функция для удаления объекта CoordinatesEntity по id
    @classmethod
    def delete_coordinates(cls, coordinates_id):
        with cls.mutex:
            coordinates = session.query(cls).get(coordinates_id)
            if coordinates:
                session.delete(coordinates)
                session.commit()

    # Функция для изменения объекта CoordinatesEntity по id
    @classmethod
    def update_coordinates(cls, coordinates_id, new_latitude, new_longitude, new_altitude):
        with cls.mutex:
            coordinates = session.query(cls).get(coordinates_id)
            if coordinates:
                coordinates.latitude = new_latitude
                coordinates.longitude = new_longitude
                coordinates.altitude = new_altitude
                session.commit()


class ExtentEntity(BaseEntity):
    __tablename__ = 'extent'

    top_left_id = Column(Integer, ForeignKey('coordinates.id', ondelete='CASCADE'))
    top_left = relationship('CoordinatesEntity', foreign_keys=[top_left_id])
    bot_left_id = Column(Integer, ForeignKey('coordinates.id', ondelete='CASCADE'))
    bot_left = relationship('CoordinatesEntity', foreign_keys=[bot_left_id])
    top_right_id = Column(Integer, ForeignKey('coordinates.id', ondelete='CASCADE'))
    top_right = relationship('CoordinatesEntity', foreign_keys=[top_right_id])
    bot_right_id = Column(Integer, ForeignKey('coordinates.id', ondelete='CASCADE'))
    bot_right = relationship('CoordinatesEntity', foreign_keys=[bot_right_id])

    # Функция для создания объекта ExtentEntity
    @classmethod
    def create_extent(cls, top_left, bot_left, top_right, bot_right):
        with cls.mutex:
            new_extent = cls(top_left_id=top_left, bot_left_id=bot_left, top_right_id=top_right, bot_right_id=bot_right)
            session.add(new_extent)
            session.commit()
            return new_extent.id

    # Функция для удаления объекта ExtentEntity по id
    @classmethod
    def delete_extent(cls, extent_id):
        with cls.mutex:
            extent = session.query(cls).get(extent_id)
            if extent:
                session.delete(extent)
                session.commit()

    # Функция для изменения объекта ExtentEntity по id
    @classmethod
    def update_extent(cls, extent_id, new_top_left, new_bot_left, new_top_right, new_bot_right):
        with cls.mutex:
            extent = session.query(cls).get(extent_id)
            if extent:
                extent.top_left_id = new_top_left
                extent.bot_left_id = new_bot_left
                extent.top_right_id = new_top_right
                extent.bot_right_id = new_bot_right
                session.commit()


class FileEntity(BaseEntity):
    __tablename__ = 'file'

    name = Column(String, nullable=False)
    path_to_file = Column(String, nullable=False)
    file_extension = Column(String)
    session_id = Column(Integer, ForeignKey('session.id', ondelete='CASCADE'))
    session = relationship('SessionEntity')

    # Функция для создания объекта FileEntity
    @classmethod
    def create_file(cls, name, path_to_file, file_extension, session_id):
        with cls.mutex:
            new_file = cls(name=name, path_to_file=path_to_file, file_extension=file_extension, session_id=session_id)
            session.add(new_file)
            session.commit()
            return new_file.id

    # Функция для удаления объекта FileEntity по id
    @classmethod
    def delete_file(cls, file_id):
        with cls.mutex:
            file = session.query(cls).get(file_id)
            if file:
                session.delete(file)
                session.commit()

    # Функция для изменения объекта FileEntity по id
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


class RawRLIEntity(BaseEntity):
    __tablename__ = 'raw_rli'

    file_id = Column(Integer, ForeignKey('file.id', ondelete='CASCADE'))
    file = relationship('FileEntity')
    type_source_rli_id = Column(Integer, ForeignKey('type_source_rli.id', ondelete='CASCADE'))
    type_source_rli = relationship('TypeSourceRLIEntity')
    date_receiving = Column(TIMESTAMP, nullable=False)

    # Функция для создания объекта RawRLIEntity
    @classmethod
    def create_raw_rli(cls, file_id, type_source_rli_id):
        with cls.mutex:
            new_raw_rli = cls(file_id=file_id, type_source_rli_id=type_source_rli_id, date_receiving=datetime.now())
            session.add(new_raw_rli)
            session.commit()
            return new_raw_rli.id

    # Функция для удаления объекта RawRLIEntity по id
    @classmethod
    def delete_raw_rli(cls, raw_rli_id):
        with cls.mutex:
            raw_rli = session.query(cls).get(raw_rli_id)
            if raw_rli:
                session.delete(raw_rli)
                session.commit()

    # Функция для изменения объекта RawRLIEntity по id
    @classmethod
    def update_raw_rli(cls, raw_rli_id, new_file_id, new_type_source_rli_id):
        with cls.mutex:
            raw_rli = session.query(cls).get(raw_rli_id)
            if raw_rli:
                raw_rli.file_id = new_file_id
                raw_rli.type_source_rli_id = new_type_source_rli_id
                raw_rli.date_receiving = datetime.now()
                session.commit()


class RLIEntity(BaseEntity):
    __tablename__ = 'rli'

    time_location = Column(TIMESTAMP)
    name = Column(String, nullable=False)
    is_processing = Column(Boolean, nullable=False, default=False)
    raw_rli_id = Column(Integer, ForeignKey('raw_rli.id', ondelete='CASCADE'))
    raw_rli = relationship('RawRLIEntity')

    # Функция для создания объекта RLIEntity
    @classmethod
    def create_rli(cls, name, is_processing, raw_rli_id):
        with cls.mutex:
            new_rli = cls(time_location=datetime.now(), name=name, is_processing=is_processing, raw_rli_id=raw_rli_id)
            session.add(new_rli)
            session.commit()
            return new_rli.id

    # Функция для удаления объекта RLIEntity по id
    @classmethod
    def delete_rli(cls, rli_id):
        with cls.mutex:
            rli = session.query(cls).get(rli_id)
            if rli:
                session.delete(rli)
                session.commit()

    # Функция для изменения объекта RLIEntity по id
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

    # Функция для получения РЛИ в сессии
    @classmethod
    def get_rli_by_session_id(cls, session_id):
        with cls.mutex:
            # Выбираем id файлов с соответствующим session_id
            ids_of_files_with_session_id = list(map(lambda x: x.id, session.query(FileEntity).
                                                    filter_by(session_id=session_id).all()))

            # Выбираем id RawRLIs по соответсвующим id файлов
            raw_rli_ids_with_session_id = list(map(lambda x: x.id, session.query(RawRLIEntity).
                                                   filter(RawRLIEntity.file_id.in_(ids_of_files_with_session_id)).all()))

            # Возваращаем соответствующие RLIs по id RawRLIs
            return session.query(cls).filter(cls.raw_rli_id.in_(raw_rli_ids_with_session_id)).all()


class RasterRLIEntity(BaseEntity):
    __tablename__ = 'raster_rli'

    rli_id = Column(Integer, ForeignKey('rli.id', ondelete='CASCADE'))
    rli = relationship('RLIEntity')
    file_id = Column(Integer, ForeignKey('file.id', ondelete='CASCADE'))
    file = relationship('FileEntity')
    extent_id = Column(Integer, ForeignKey('extent.id', ondelete='CASCADE'))
    extent = relationship('ExtentEntity')

    # Функция создания объекта RasterRLIEntity
    @classmethod
    def create_raster_rli(cls, rli_id, file_id, extent_id):
        with cls.mutex:
            new_raster_rli = cls(rli_id=rli_id, file_id=file_id, extent_id=extent_id)
            session.add(new_raster_rli)
            session.commit()
            return new_raster_rli.id

    # Функция для удаления объекта RasterRLIEntity по id
    @classmethod
    def delete_raster_rli(cls, raster_rli_id):
        with cls.mutex:
            raster_rli = session.query(cls).get(raster_rli_id)
            if raster_rli:
                session.delete(raster_rli)
                session.commit()

    # Функция для изменения объекта RasterRLIEntity по id
    @classmethod
    def update_raster_rli(cls, raster_rli_id, new_rli_id, new_file_id, new_extent_id):
        with cls.mutex:
            raster_rli = session.query(cls).get(raster_rli_id)
            if raster_rli:
                raster_rli.rli_id = new_rli_id
                raster_rli.file_id = new_file_id
                raster_rli.extent_id = new_extent_id
                session.commit()


class TypeBindingMethodEntity(BaseEntity):
    __tablename__ = 'type_binding_method'

    name = Column(String, nullable=False)

    # Функция для создания объекта TypeBindingMethodEntity
    @classmethod
    def create_type_binding_method(cls, name):
        with cls.mutex:
            new_type_binding_method = cls(name=name)
            session.add(new_type_binding_method)
            session.commit()
            return new_type_binding_method.id

    # Функция для удаления объекта TypeBindingMethodEntity по id
    @classmethod
    def delete_type_binding_method(cls, type_binding_method_id):
        with cls.mutex:
            type_binding_method = session.query(cls).get(type_binding_method_id)
            if type_binding_method:
                session.delete(type_binding_method)
                session.commit()

    # Функция для изменения объекта TypeBindingMethodEntity по id
    @classmethod
    def update_type_binding_method(cls, type_binding_method_id, new_name):
        with cls.mutex:
            type_binding_method = session.query(cls).get(type_binding_method_id)
            if type_binding_method:
                type_binding_method.name = new_name
                session.commit()


class LinkedRLIEntity(BaseEntity):
    __tablename__ = 'linked_rli'

    raster_rli_id = Column(Integer, ForeignKey('raster_rli.id', ondelete='CASCADE'))
    raster_rli = relationship('RasterRLIEntity')
    file_id = Column(Integer, ForeignKey('file.id', ondelete='CASCADE'))
    file = relationship('FileEntity')
    extent_id = Column(Integer, ForeignKey('extent.id', ondelete='CASCADE'))
    extent = relationship('ExtentEntity')
    binding_attempt_number = Column(Integer)
    type_binding_method_id = Column(Integer, ForeignKey('type_binding_method.id', ondelete='CASCADE'))
    type_binding_method = relationship('TypeBindingMethodEntity')

    # Функция для создания объекта LinkedRLIEntity
    @classmethod
    def create_linked_rli(cls, raster_rli_id, file_id, extent_id, binding_attempt_number, type_binding_method_id):
        with cls.mutex:
            new_linked_rli = cls(raster_rli_id=raster_rli_id, file_id=file_id, extent_id=extent_id,
                                 binding_attempt_number=binding_attempt_number,
                                 type_binding_method_id=type_binding_method_id)
            session.add(new_linked_rli)
            session.commit()
            return new_linked_rli.id

    # Функция для удаления объекта LinkedRLIEntity по id
    @classmethod
    def delete_linked_rli(cls, linked_rli_id):
        with cls.mutex:
            linked_rli = session.query(cls).get(linked_rli_id)
            if linked_rli:
                session.delete(linked_rli)
                session.commit()

    # Функция для изменения объекта LinkedRLIEntity по id
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

    # Функция для получения привязанных РЛИ в сессии
    @classmethod
    def get_linked_rli_by_session_id(cls, session_id):
        with cls.mutex:
            # Выбираем id файлов с соответствующим session_id
            ids_of_files_with_session_id = list(map(lambda x: x.id, session.query(FileEntity).
                                                    filter_by(session_id=session_id).all()))

            # Возвращаем соответствующие LinkedRLIs по file_id
            return session.query(cls).filter(cls.file_id.in_(ids_of_files_with_session_id)).all()


class MarkEntity(BaseEntity):
    __tablename__ = 'mark'

    coordinates_id = Column(Integer, ForeignKey('coordinates.id', ondelete='CASCADE'))
    coordinates = relationship('CoordinatesEntity')
    datetime = Column(TIMESTAMP, nullable=False)
    session_id = Column(Integer, ForeignKey('session.id', ondelete='CASCADE'))
    session = relationship('SessionEntity')

    # Функция для создания объекта MarkEntity
    @classmethod
    def create_mark(cls, coordinates_id, session_id):
        with cls.mutex:
            new_mark = cls(coordinates_id=coordinates_id, datetime=datetime.now(), session_id=session_id)
            session.add(new_mark)
            session.commit()
            return new_mark.id

    # Функция для удаления объекта MarkEntity по id
    @classmethod
    def delete_mark(cls, mark_id):
        with cls.mutex:
            mark = session.query(cls).get(mark_id)
            if mark:
                session.delete(mark)
                session.commit()

    # Функция для изменения объекта MarkEntity по id
    @classmethod
    def update_mark(cls, mark_id, new_coordinates_id, new_session_id):
        with cls.mutex:
            mark = session.query(cls).get(mark_id)
            if mark:
                mark.coordinates_id = new_coordinates_id
                mark.datetime = datetime.now()
                mark.session_id = new_session_id
                session.commit()

    # Функция получения отметок
    @classmethod
    def get_all_marks(cls):
        with cls.mutex:
            return session.query(cls).all()

    # Функция получения отметок сессии
    @classmethod
    def get_marks_by_session_id(cls, session_id):
        return session.query(cls).filter(cls.session_id == session_id).all()


class RelatingObjectEntity(BaseEntity):
    __tablename__ = 'relating_object'

    type_relating = Column(Integer, nullable=False)
    name = Column(String, nullable=False)

    # Функция для создания объекта RelatingObjectEntity
    @classmethod
    def create_relating_object(cls, type_relating, name):
        with cls.mutex:
            new_relating_object = cls(type_relating=type_relating, name=name)
            session.add(new_relating_object)
            session.commit()
            return new_relating_object.id

    # Функция для удаления объекта RelatingObjectEntity по id
    @classmethod
    def delete_relating_object(cls, relating_object_id):
        with cls.mutex:
            relating_object = session.query(cls).get(relating_object_id)
            if relating_object:
                session.delete(relating_object)
                session.commit()

    # Функция для изменения объекта RelatingObjectEntity по id
    @classmethod
    def update_relating_object(cls, relating_object_id, new_type_relating, new_name):
        with cls.mutex:
            relating_object = session.query(cls).get(relating_object_id)
            if relating_object:
                relating_object.type_relating = new_type_relating
                relating_object.name = new_name
                session.commit()


class ObjectEntity(BaseEntity):
    __tablename__ = 'object'

    mark_id = Column(Integer, ForeignKey('mark.id', ondelete='CASCADE'))
    mark = relationship('MarkEntity')
    name = Column(String)
    type = Column(String)
    relating_object_id = Column(Integer, ForeignKey('relating_object.id', ondelete='CASCADE'))
    relating_object = relationship('RelatingObjectEntity')
    meta = Column(JSON)

    # Функция для создания объекта ObjectEntity
    @classmethod
    def create_object(cls, mark_id, name, object_type, relating_object_id, meta):
        with cls.mutex:
            new_object = cls(mark_id=mark_id, name=name, type=object_type,
                             relating_object_id=relating_object_id, meta=meta)
            session.add(new_object)
            session.commit()
            return new_object.id

    # Функция для удаления объекта ObjectEntity по id
    @classmethod
    def delete_object(cls, object_id):
        with cls.mutex:
            object_ = session.query(cls).get(object_id)
            if object_:
                session.delete(object_)
                session.commit()

    # Функция для изменения объекта ObjectEntity по id
    @classmethod
    def update_object(cls, object_id, new_mark_id, new_name, new_object_type, new_relating_object_id, new_meta):
        with cls.mutex:
            object_ = session.query(cls).get(object_id)
            if object_:
                object_.mark_id = new_mark_id
                object_.name = new_name
                object_.type = new_object_type
                object_.relating_object_id = new_relating_object_id
                object_.meta = new_meta
                session.commit()


class TargetEntity(BaseEntity):
    __tablename__ = 'target'

    number = Column(Integer, nullable=False)
    object_id = Column(Integer, ForeignKey('object.id', ondelete='CASCADE'))
    object = relationship('ObjectEntity')
    raster_rli_id = Column(Integer, ForeignKey('raster_rli.id', ondelete='CASCADE'))
    raster_rli = relationship('RasterRLIEntity')
    datetime_sending = Column(TIMESTAMP)
    sppr_type_key = Column(String)

    # Функция для создания объекта TargetEntity
    @classmethod
    def create_target(cls, number, object_id, raster_rli_id, sppr_type_key):
        with cls.mutex:
            new_target = cls(number=number, object_id=object_id, raster_rli_id=raster_rli_id,
                             datetime_sending=datetime.now(), sppr_type_key=sppr_type_key)
            session.add(new_target)
            session.commit()
            return new_target.id

    # Функция для удаления объекта TargetEntity по id
    @classmethod
    def delete_target(cls, target_id):
        with cls.mutex:
            target = session.query(cls).get(target_id)
            if target:
                session.delete(target)
                session.commit()

    # Функция для изменения объекта TargetEntity по id
    @classmethod
    def update_target(cls, target_id, new_number, new_object_id, new_raster_rli_id, new_sppr_type_key):
        with cls.mutex:
            target = session.query(cls).get(target_id)
            if target:
                target.number = new_number
                target.object_id = new_object_id
                target.raster_rli_id = new_raster_rli_id
                target.datetime_sending = datetime.now()
                target.sppr_type_key = new_sppr_type_key
                session.commit()

    # Функция для получения целей сессии
    @classmethod
    def get_targets_by_session_id(cls, session_id):
        with cls.mutex:
            # Выбираем id файлов с соответствующим session_id
            ids_of_files_with_session_id = list(map(lambda x: x.id, session.query(FileEntity).
                                                    filter_by(session_id=session_id).all()))

            # Выбираем id RasterRLIs по соответсвующим id файлов
            raster_rli_ids_with_session_id = list(map(lambda x: x.id, session.query(RasterRLIEntity).
                                                      filter(RasterRLIEntity.file_id.in_(ids_of_files_with_session_id)).
                                                      all()))

            # Возваращаем соответствующие Targets по id RasterRLIs
            return session.query(cls).filter(cls.raster_rli_id.in_(raster_rli_ids_with_session_id)).all()


class RegionEntity(BaseEntity):
    __tablename__ = 'region'

    extent_id = Column(Integer, ForeignKey('extent.id', ondelete='CASCADE'))
    extent = relationship('ExtentEntity')
    name = Column(String)

    # Функция для создания объекта RegionEntity
    @classmethod
    def create_region(cls, extent_id, name):
        with cls.mutex:
            new_region = cls(extent_id=extent_id, name=name)
            session.add(new_region)
            session.commit()
            return new_region.id

    # Функция для удаления объекта RegionEntity по id
    @classmethod
    def delete_region(cls, region_id):
        with cls.mutex:
            region_ = session.query(cls).get(region_id)
            if region:
                session.delete(region_)
                session.commit()

    # Функция для изменения объекта RegionEntity по id
    @classmethod
    def update_region(cls, region_id, new_extent_id, new_name):
        with cls.mutex:
            region_ = session.query(cls).get(region_id)
            if region_:
                region_.extent_id = new_extent_id
                region_.name = new_name
                session.commit()

    # Функция получения регионов
    @classmethod
    def get_all_regions(cls):
        with cls.mutex:
            return session.query(cls).all()


# Создание таблиц
Base.metadata.create_all(bind=engine)

# Проверка работы методов

# TypeSessions

TypeSessionEntity.create_type_session("Type 1")
print(session.query(TypeSessionEntity).get(1).name)
TypeSessionEntity.create_type_session("Type 2")
print(session.query(TypeSessionEntity).get(2).name)
TypeSessionEntity.update_type_session(1, "New SessionEntity")
TypeSessionEntity.update_type_session(2, "New SessionEntity 2")
print(session.query(TypeSessionEntity).get(1).name)
print(session.query(TypeSessionEntity).get(2).name)
# TypeSessionEntity.delete_type_session(1)
# TypeSessionEntity.delete_type_session(2)
# try:
#     print(session.query(TypeSessionEntity).get(1).name)
#     print(session.query(TypeSessionEntity).get(2).name)
# except:
#     print("No such TypeSessions")

print()

# TypeSourceRLIs

TypeSourceRLIEntity.create_type_source_rli("TypeSourceRLIEntity 1")
print(session.query(TypeSourceRLIEntity).get(1).name)
TypeSourceRLIEntity.create_type_source_rli("TypeSourceRLIEntity 2")
print(session.query(TypeSourceRLIEntity).get(2).name)
TypeSourceRLIEntity.update_type_source_rli(1, "New TypeSourceRLIEntity")
TypeSourceRLIEntity.update_type_source_rli(2, "New TypeSourceRLIEntity 2")
print(session.query(TypeSourceRLIEntity).get(1).name)
print(session.query(TypeSourceRLIEntity).get(2).name)
# TypeSourceRLIEntity.delete_type_source_rli(1)
# TypeSourceRLIEntity.delete_type_source_rli(2)
# try:
#     print(session.query(TypeSourceRLIEntity).get(1).name)
#     print(session.query(TypeSourceRLIEntity).get(2).name)
# except:
#     print("No such TypeSourceRLIs")

print()

# SessionEntity

SessionEntity.create_session("SessionEntity 1", "/some/some/session_1", session.query(TypeSessionEntity).get(1).id)


print(session.query(SessionEntity).get(1).name, session.query(SessionEntity).get(1).path_to_directory,
      session.query(SessionEntity).get(1).type_session_id, session.query(SessionEntity).get(1).date)
SessionEntity.create_session("SessionEntity 2", "/some/some/session_2", session.query(TypeSessionEntity).get(2).id)
print(session.query(SessionEntity).get(2).name, session.query(SessionEntity).get(2).path_to_directory,
      session.query(SessionEntity).get(2).type_session_id, session.query(SessionEntity).get(2).date)
SessionEntity.update_session(1, "Update SessionEntity 1", "/some/some/update_session_1", session.query(TypeSessionEntity).get(2).id)
SessionEntity.update_session(2, "Update SessionEntity 2", "/some/some/update_session_2", session.query(TypeSessionEntity).get(1).id)
print(session.query(SessionEntity).get(1).name, session.query(SessionEntity).get(1).path_to_directory,
      session.query(SessionEntity).get(1).type_session_id, session.query(SessionEntity).get(1).date)
print(session.query(SessionEntity).get(2).name, session.query(SessionEntity).get(2).path_to_directory,
      session.query(SessionEntity).get(2).type_session_id, session.query(SessionEntity).get(2).date)
print(SessionEntity.get_all_sessions())
# SessionEntity.delete_session(1)
# SessionEntity.delete_session(2)
# try:
#     print(session.query(SessionEntity).get(1).name)
#     print(session.query(SessionEntity).get(2).name)
# except:
#     print("No such Sessions")

# CoordinatesEntity

CoordinatesEntity.create_coordinates(56.24112, 54.12331, 45.4214)
CoordinatesEntity.create_coordinates(46.24212, 44.1231, 47.4214)
print(session.query(CoordinatesEntity).get(1).latitude)
print(session.query(CoordinatesEntity).get(2).altitude)
CoordinatesEntity.update_coordinates(1, 24.5225, 34.252, 56.1242)
CoordinatesEntity.update_coordinates(2, 42.5225, 33.252, 76.1242)
print(session.query(CoordinatesEntity).get(1).longitude)
print(session.query(CoordinatesEntity).get(2).latitude)
# CoordinatesEntity.delete_coordinates(1)
# CoordinatesEntity.delete_coordinates(2)
# try:
#     print(session.query(CoordinatesEntity).get(1).latitude)
#     print(session.query(CoordinatesEntity).get(2).latitude)
# except:
#     print("No such CoordinatesEntity")

# ExtentEntity

ExtentEntity.create_extent(1, 1, 2, 2)
ExtentEntity.create_extent(2, 2, 1, 1)
print(session.query(CoordinatesEntity).get(session.query(ExtentEntity).get(1).top_left_id))
print(session.query(CoordinatesEntity).get(session.query(ExtentEntity).get(2).bot_left_id))
ExtentEntity.update_extent(1, 2, 2, 2, 2)
ExtentEntity.update_extent(2, 1, 1, 1, 1)
print(session.query(CoordinatesEntity).get(session.query(ExtentEntity).get(1).top_left_id))
print(session.query(CoordinatesEntity).get(session.query(ExtentEntity).get(2).bot_left_id))
# ExtentEntity.delete_extent(1)
# ExtentEntity.delete_extent(2)
# try:
#     print(session.query(ExtentEntity).get(1).top_left_id)
#     print(session.query(ExtentEntity).get(2).top_left_id)
# except:
#     print("No such Extents")

print()

# FileEntity

FileEntity.create_file("FileEntity 1", "path_to_file", "file_extension", 1)
FileEntity.create_file("FileEntity 2", "path_to_file", "file_extension", 2)
print(session.query(FileEntity).get(1).name, session.query(FileEntity).get(1).path_to_file)
print(session.query(FileEntity).get(2).session_id)
FileEntity.update_file(1, "New FileEntity 1", "new_path_to_file", "new_file_extension", 2)
FileEntity.update_file(2, "New FileEntity 2", "new_path_to_file", "new_file_extension", 1)
print(session.query(FileEntity).get(1).name, session.query(FileEntity).get(1).path_to_file)
print(session.query(FileEntity).get(2).session_id)
# FileEntity.delete_file(1)
# FileEntity.delete_file(2)
# try:
#     print(session.query(FileEntity).get(1).name, session.query(FileEntity).get(1).path_to_file)
#     print(session.query(FileEntity).get(2).session_id)
# except:
#     print("No such files")

print()

# RawRLIEntity

RawRLIEntity.create_raw_rli(1, 1)
RawRLIEntity.create_raw_rli(2, 2)
print(session.query(RawRLIEntity).get(1).type_source_rli_id)
print(session.query(RawRLIEntity).get(2).file_id, session.query(RawRLIEntity).get(2).date_receiving)
RawRLIEntity.update_raw_rli(1, 2, 2)
RawRLIEntity.update_raw_rli(2, 1, 1)
print(session.query(RawRLIEntity).get(1).type_source_rli_id)
print(session.query(RawRLIEntity).get(2).file_id)
# RawRLIEntity.delete_raw_rli(1)
# RawRLIEntity.delete_raw_rli(2)
# try:
#     print(session.query(RawRLIEntity).get(1).type_source_rli_id)
#     print(session.query(RawRLIEntity).get(2).file_id)
# except:
#     print("No such RLIs")

print()

# RLIEntity

RLIEntity.create_rli("RLIEntity 1", True, 1)
RLIEntity.create_rli("RLIEntity 2", False, 2)
print(session.query(RLIEntity).get(1).time_location, session.query(RLIEntity).get(1).name,
      session.query(RLIEntity).get(1).is_processing, session.query(RLIEntity).get(1).raw_rli_id)
print(session.query(RLIEntity).get(2).time_location, session.query(RLIEntity).get(2).name,
      session.query(RLIEntity).get(2).is_processing, session.query(RLIEntity).get(2).raw_rli_id)
RLIEntity.update_rli(2, " New RLIEntity 2", True, 2)
print(session.query(RLIEntity).get(2).time_location, session.query(RLIEntity).get(2).name,
      session.query(RLIEntity).get(2).is_processing, session.query(RLIEntity).get(2).raw_rli_id)

print(RLIEntity.get_rli_by_session_id(1))

print()

# RasterRLIEntity

RasterRLIEntity.create_raster_rli(1, 1, 1)
RasterRLIEntity.create_raster_rli(2, 2, 2)
print(session.query(RasterRLIEntity).get(1).extent_id)
RasterRLIEntity.update_raster_rli(1, 2, 2, 2)
print(session.query(RasterRLIEntity).get(1).file_id)
# RasterRLIEntity.delete_raster_rli(1)
# try:
#     print(session.query(RasterRLIEntity).get(1).file_id)
# except:
#     print("No such RasterRLIs")

print()

# LinkedRLIEntity

LinkedRLIEntity.create_linked_rli(1, 1, 1, 1, 1)
LinkedRLIEntity.create_linked_rli(2, 2, 2, 2, 2)
print(session.query(LinkedRLIEntity).get(1).file_id)
print(session.query(LinkedRLIEntity).get(2).extent_id)
print(LinkedRLIEntity.get_linked_rli_by_session_id(1))
LinkedRLIEntity.update_linked_rli(1, 2, 2, 2, 2, 2)
LinkedRLIEntity.update_linked_rli(2, 1, 1, 1, 1, 1)
print(session.query(LinkedRLIEntity).get(1).file_id)
print(session.query(LinkedRLIEntity).get(2).extent_id)
# LinkedRLIEntity.delete_linked_rli(1)
# LinkedRLIEntity.delete_linked_rli(2)
# try:
#     print(session.query(LinkedRLIEntity).get(1).file_id)
#     print(session.query(LinkedRLIEntity).get(2).extent_id)
# except:
#     print("No such LinkedRLIs")

print()

# MarkEntity

MarkEntity.create_mark(1, 1)
MarkEntity.create_mark(2, 2)
print(session.query(MarkEntity).get(1).coordinates_id)
print(session.query(MarkEntity).get(2).session_id)
print(MarkEntity.get_all_marks())
print(MarkEntity.get_marks_by_session_id(1))
MarkEntity.update_mark(1, 2, 2)
MarkEntity.update_mark(2, 1, 1)
print(session.query(MarkEntity).get(1).coordinates_id)
print(session.query(MarkEntity).get(2).session_id)
# MarkEntity.delete_mark(1)
# MarkEntity.delete_mark(2)
# try:
#     print(session.query(MarkEntity).get(1).coordinates_id)
#     print(session.query(MarkEntity).get(2).session_id)
# except:
#     print("No such marks")

print()

# RelatingObjectEntity

RelatingObjectEntity.create_relating_object(1, "Relating ObjectEntity")
print(session.query(RelatingObjectEntity).get(1).name)
RelatingObjectEntity.update_relating_object(1, 42, "New Relating ObjectEntity")
print(session.query(RelatingObjectEntity).get(1).type_relating)
# RelatingObjectEntity.delete_relating_object(1)
# try:
#     print(session.query(RelatingObjectEntity).get(1).name)
# except:
#     print("No such RelatingObjectEntity")

print()

# ObjectEntity

ObjectEntity.create_object(1, "object", "object_type", 1, "{meta: meta}")
ObjectEntity.create_object(2, "object 2", "object_type_2", 1, "{meta: meta}")
print(session.query(ObjectEntity).get(1).meta)
print(session.query(ObjectEntity).get(2).type)
ObjectEntity.update_object(1, 1, "object 1", "object_type 1", 1, "{meta: meta}")
ObjectEntity.update_object(2, 2, "new object 2", "new_object_type_2", 1, "{meta: meta}")
print(session.query(ObjectEntity).get(1).type)
print(session.query(ObjectEntity).get(2).name)
# ObjectEntity.delete_object(1)
# ObjectEntity.delete_object(2)
# try:
#     print(session.query(ObjectEntity).get(1).type)
#     print(session.query(ObjectEntity).get(2).name)
# except:
#     print("No such objects")

print()

# TargetEntity

TargetEntity.create_target(1, 1, 1, "type_key")
TargetEntity.create_target(2, 2, 2, "type_key")
print(session.query(TargetEntity).get(1).sppr_type_key)
print(session.query(TargetEntity).get(2).object_id)
print(TargetEntity.get_targets_by_session_id(1))
TargetEntity.update_target(1, 2, 2, 2, "new_type_key")
print(session.query(TargetEntity).get(1).sppr_type_key)
TargetEntity.delete_target(1)
TargetEntity.delete_target(2)
try:
    print(session.query(TargetEntity).get(1).sppr_type_key)
    print(session.query(TargetEntity).get(2).object_id)
except:
    print("No such targets")

print()

# RegionEntity

RegionEntity.create_region(1, "Moscow")
RegionEntity.create_region(2, "Minsk")
print(session.query(RegionEntity).get(1))
print(session.query(RegionEntity).get(2))
for region in RegionEntity.get_all_regions():
    print(region.name)

RegionEntity.update_region(1, 2, "Astana")
RegionEntity.update_region(2, 1, "Vladivostok")
for region in RegionEntity.get_all_regions():
    print(region.name)

RegionEntity.delete_region(1)
RegionEntity.delete_region(2)
try:
    print(session.query(RegionEntity).get(1).name)
    print(session.query(RegionEntity).get(2).name)
except:
    print("No such regions")

print()

# TypeBindingMethodEntity

TypeBindingMethodEntity.create_type_binding_method("Type Binding Method")
print(session.query(TypeBindingMethodEntity).get(1).name)
TypeBindingMethodEntity.update_type_binding_method(1, "New Type Binding Method")
print(session.query(TypeBindingMethodEntity).get(1).name)
TypeBindingMethodEntity.delete_type_binding_method(1)
try:
    print(session.query(TypeBindingMethodEntity).get(1).name)
except:
    print("No such TypeBindingMethods")

