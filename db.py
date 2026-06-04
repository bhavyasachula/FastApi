from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

url = "postgresql://postgres:bhavya@localhost:5432/MyProjectDb"
engine = create_engine(url)
session = sessionmaker(autoflush=False,autocommit=False,bind=engine)
