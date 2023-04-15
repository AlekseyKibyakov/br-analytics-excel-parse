import sqlalchemy as sq
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

def create_tables(engine):
    Base.metadata.create_all(engine)


class Message(Base):
    __tablename__ = 'message'

    
    
    def __str__(self):
        return [
            
            ]


class Author(Base):
    __tablename__ = 'author'

    
    
    def __str__(self):
        return [
            
            ]

class Tag(Base):
    __tablename__ = 'tag'

    
    
    def __str__(self):
        return [
            
            ]