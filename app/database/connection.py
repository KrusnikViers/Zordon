from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from app import config
from app.database import updater


engine: Engine = None
Session = sessionmaker()


def initialise(database_url: str = None):
    global engine, Session
    engine = create_engine(database_url if database_url else config.DATABASE_URL)
    Session.configure(bind=engine)
    updater.run_migrations()
