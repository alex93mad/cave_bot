import sqlalchemy as sa
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.inspection import inspect
from sqlite3 import Connection as SQLite3Connection

from .const import UserRole as ur, DEFAULT_USER_CONFIG
from .utils import copy_dict_with_exclude

def get_engine(db_connection_str):
   echo = False
   engine = sa.create_engine(db_connection_str, echo = echo)
   print(f'created engine {engine.url}')
   if not database_exists(engine.url): create_database(engine.url)
   return engine

@sa.event.listens_for(sa.engine.Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

class Db:
   def __init__(self, models, db_connection_str):
      self.m = models
      self.memory_db = sa.create_engine("sqlite://")
      self.load_db = get_engine(db_connection_str)

      self.m.Base.metadata.create_all(self.memory_db)
      self.m.Base.metadata.create_all(self.load_db)

      self.load_from_one_db_to_another(self.load_db, self.memory_db)

      self.Session = self.get_session(self.memory_db)
      self.LoadSession = self.get_session(self.load_db)

      with self.Session() as s:
         last_scan_record = s.query(self.m.LastScan).first()
         print(f'last_scan: {str(last_scan_record and last_scan_record.last_scan)}')

   def drop_tables(self):
      self.m.Base.metadata.drop_all(bind = self.load_db)

   def get_session(self, engine):
      Session = sa.orm.sessionmaker()
      Session.configure(bind=engine)
      return Session
   
   def query_record_by_hash_and_model(self, hash, model, session):
      primary_keys = [key.name for key in inspect(model).primary_key]
      filters = {}
      for pk in primary_keys:
         if pk not in hash:
            # as example autogenerated ids
            continue
         filters[pk] = hash[pk]
      if len(filters.keys()) == 0:
         # if the only one primaryKey - autogenerated - was not in hash - then we won't found it in db
         return None
      record = session.query(model).filter_by(**filters).first()
      return record

   def add_record_to_load_db_by_record(self, record, model):
      relationships = inspect(model).relationships.keys()
      hash = copy_dict_with_exclude(record.__dict__, ['_sa_instance_state', *relationships])
      with self.LoadSession() as s:
         obj = self.query_record_by_hash_and_model(hash, model, s)
         if obj is None:
            obj = model(**hash)

         for k, v in hash.items():
            setattr(obj, k, v)
            
         s.add(obj)
         s.commit()

   def delete_record_from_load_db_by_record(self, record, model):
      hash = copy_dict_with_exclude(record.__dict__, ['_sa_instance_state'])
      with self.LoadSession() as s:
         obj = self.query_record_by_hash_and_model(hash, model, s)
         if obj:
            s.delete(obj)
            s.commit()

   def save_to_load_db(self):
      self.load_from_one_db_to_another(self.memory_db, self.load_db)

   def load_from_one_db_to_another(self, engine_from, engine_to):
      with engine_from.connect() as db_from:
         with engine_to.connect() as db_to:
            for table in self.m.Base.metadata.sorted_tables:
               db_to.execute(table.delete())
               for row in db_from.execute(sa.select(table.c)):
                  db_to.execute(table.insert().values(row._mapping))
            db_to.commit()