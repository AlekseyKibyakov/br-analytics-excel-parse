import sqlalchemy as sq
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

def create_tables(engine):
    Base.metadata.create_all(engine)


class Message(Base):
    __tablename__ = 'message'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    id_Сообщения = sq.Column(sq.VARCHAR(100000), unique=True)
    Дата = sq.Column(sq.VARCHAR(10000))
    Заголовок = sq.Column(sq.VARCHAR(5000))
    Текст = sq.Column(sq.VARCHAR(100000))
    Url = sq.Column(sq.VARCHAR(10000))
    Автор = sq.Column(sq.VARCHAR(10000))
    Url_автора = sq.Column(sq.VARCHAR(10000))
    Тип_автора = sq.Column(sq.VARCHAR(500))
    Пол = sq.Column(sq.VARCHAR(500))
    Возраст = sq.Column(sq.Integer)
    Тип_сообщения = sq.Column(sq.VARCHAR(500))
    Источник  = sq.Column(sq.VARCHAR(10000))
    Тип_источника = sq.Column(sq.VARCHAR(1000))
    Место_публикации = sq.Column(sq.VARCHAR(10000))
    Url_места_публикации = sq.Column(sq.VARCHAR(10000))
    Аудитория = sq.Column(sq.Integer)
    Комментариев = sq.Column(sq.Integer)
    Цитируемость = sq.Column(sq.Integer)
    Репостов = sq.Column(sq.Integer)
    Лайков = sq.Column(sq.Integer)
    Вовлеченность = sq.Column(sq.Integer)
    Просмотров = sq.Column(sq.Integer)
    Оценка = sq.Column(sq.Integer)
    Дублей = sq.Column(sq.Integer)
    Тональность = sq.Column(sq.VARCHAR(1000))
    Роль_объекта = sq.Column(sq.VARCHAR(1000))
    Агрессия = sq.Column(sq.Boolean, default=False)
    Страна = sq.Column(sq.VARCHAR(10000))
    Регион = sq.Column(sq.VARCHAR(10000))
    Город = sq.Column(sq.VARCHAR(10000))
    Место = sq.Column(sq.VARCHAR(10000))
    Адрес = sq.Column(sq.VARCHAR(10000))
    Язык = sq.Column(sq.VARCHAR(1000))
    WOM = sq.Column(sq.Boolean, default=False)
    Обработано = sq.Column(sq.Boolean)
    Теги = relationship('Tag', secondary='message_tag', backref='messages', cascade='delete')
    def __str__(self):
        return [
            self.id_Сообщения
            ]    
    

# class Author(Base):
#     __tablename__ = 'author'
    

    
#     def __str__(self):
#         return [
#             self.Автор
#             ]


class Tag(Base):
    __tablename__ = 'tag'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    Название = sq.Column(sq.VARCHAR(100), unique=True)
    
    def __str__(self):
        return [
            self.Название
            ]


class message_tag(Base):
    __tablename__ = 'message_tag'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    Сообщение = sq.Column(sq.VARCHAR(100), sq.ForeignKey('message.id_Сообщения'))
    Тег = sq.Column(sq.VARCHAR(100), sq.ForeignKey('tag.Название'))
  

# message_tag = sq.Table('message_tag',
#                        Base.metadata,
#                        sq.Column('message_id',sq.Integer, sq.ForeignKey('message.id'), primary_key=True),
#                        sq.Column('tag_id',sq.Integer, sq.ForeignKey('tag.id'), primary_key=True),
#                        sq.Column('flag'),sq.Boolean)




# class Source(Base):
#     __tablename__ = 'source'


    
#     def __str__(self):
#         return [
#             self.Источник
#             ]