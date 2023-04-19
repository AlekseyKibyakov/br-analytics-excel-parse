import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from config import DB_LOGIN, CONNSTR
from models import create_tables, message_tag
from models import Message, Tag

DSN = f'postgresql://{DB_LOGIN["login"]}:\
{DB_LOGIN["password"]}@{DB_LOGIN["host"]}:\
{DB_LOGIN["port"]}/{DB_LOGIN["database"]}'

engine = sq.create_engine(DSN)
create_tables(engine)
Session = sessionmaker(bind=engine)
session = Session()

def _check_is_in_db(object):
    if isinstance(object, Message):
        for el in session.query(Message).all():
            if el.id_Сообщения == str(object.id_Сообщения):
                return True
    elif isinstance(object, Tag):
        for el in session.query(Tag).all():
            if el.Название == object.Название:
                return True
    elif isinstance(object, message_tag):
        for el in session.query(message_tag).all():
            if el.message_id == object.message_id and el.tag_id == object.tag_id:
                return True

    return False


def add_tags_to_message(message_id, tags_list):
    message = session.query(Message).filter(Message.id_Сообщения == str(message_id)).first()
    for tag_name in tags_list:
        tag = session.query(Tag).filter(Tag.Название == tag_name).first()
        message.Теги.append(tag)
    
    session.commit()


def get_tags():
    return session.query(Tag).all()


def add_to_db(object):
    if _check_is_in_db(object):
        session.close()
        return
    session.add(object)
    session.commit()
