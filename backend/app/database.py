from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

URL_CONNECTION = 'postgresql+psycopg2://postgres:12345@localhost/DBProyectoSuper'

engine = create_engine(URL_CONNECTION)

SessionLocal = sessionmaker(autoflush = False, autocommit=False, bind=engine)

Base = declarative_base()