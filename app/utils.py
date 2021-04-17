import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


def db_init(env:dict):
    engine = sa.create_engine(env["DATABASE_URI"])
    Base = declarative_base(bind=engine, metadata=sa.MetaData(naming_convention=naming_convention))
    Session = sessionmaker(bind = engine)
    #session = Session()
    #return {
    #    "engine" : engine,
    #    "base": Base,
    #    "session": session
    #}
    return engine, Base, Session
