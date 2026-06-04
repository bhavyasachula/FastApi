from sqlalchemy import Column,Integer,String,Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    # To name the table by sqlalchemy
    __tablename__ = "product"
    # using column to identify by the sqlalchemy
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    description=Column(String)
    price=Column(Float)
    quantity=Column(Integer)
