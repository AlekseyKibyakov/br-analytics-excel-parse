import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from config import DB_LOGIN
from models import create_tables

DSN = f'postgresql://{DB_LOGIN["login"]}:\
{DB_LOGIN["password"]}@{DB_LOGIN["host"]}:\
{DB_LOGIN["port"]}/{DB_LOGIN["database"]}'

engine = sq.create_engine(DSN)
create_tables(engine)
Session = sessionmaker(bind=engine)
session = Session()
