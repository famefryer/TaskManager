from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_USERNAME = 'postgres'
DB_PASSWORD = 'famefryer'
DB_NAME = 'task_management'
DB_URL = 'localhost:5432'
SQLALCHEMY_DB_URL = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_URL}/{DB_NAME}'

engine = create_engine(SQLALCHEMY_DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
