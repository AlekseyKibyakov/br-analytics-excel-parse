import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from config import DB_LOGIN
from models import create_tables
from models import Message, Tag

DSN = f'postgresql://{DB_LOGIN["login"]}:\
{DB_LOGIN["password"]}@{DB_LOGIN["host"]}:\
{DB_LOGIN["port"]}/{DB_LOGIN["database"]}'

engine = sq.create_engine(DSN)
create_tables(engine)
Session = sessionmaker(bind=engine)
session = Session()

def add_tags_to_message(message_id, tags):
    session.commit()
    message = session.query(Message).filter(Message.id_Сообщения == str(message_id)).first()
    for tag_name in tags:
        if tag_name:
            tag = session.query(Tag).filter(Tag.Название == tag_name).first()
            message.Теги.append(tag)


def close_session():
    session.close()
    

def add_to_db(object):
    session.add(object)
