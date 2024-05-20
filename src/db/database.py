from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings import db_url, db_name, db_password, db_username

SQLALCHEMY_DB_URL = f'postgresql://{db_username}:{db_password}@{db_url}/{db_name}'

engine = create_engine(SQLALCHEMY_DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
