from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

URL_CONNECTION = 'postgresql+psycopg2://postgres:1234@localhost/ProyectoSuper'

engine = create_engine(URL_CONNECTION)

localSession = sessionmaker(autoflush = False, autocommit=False, bind=engine)

#el nombre de base puede cambiar
Base = declarative_base()