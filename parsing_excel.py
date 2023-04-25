from db_interaction import add_to_db, add_tags_to_message, close_session
import openpyxl as oxl
import re
from loguru import logger
from models import Message, Tag
import numpy as np


def open_excel():
    '''Open excel sheet and build numpy array'''
    file = 'report.xlsx'
    wb = oxl.load_workbook(file, read_only=True)
    sh = wb.worksheets[1]
    np_sh = np.array([[i for i in j] for j in sh.iter_rows(min_row=6, min_col=2, values_only=True)])
    return np_sh    


def parse_tags(np_sh):
    '''Get all tags from current worksheet'''
    max_col = np_sh.shape[1]
    for column in range(35, max_col):
        try:
            tag = Tag(Название = np_sh[0, column])
            add_to_db(tag)
            logger.info(f"Add {tag.Название} tag")
        except BaseException as er:
            logger.error(er)
            continue

def parse_messages(np_sh):
    '''Create message object and add tags into it'''
    max_col = np_sh.shape[1]
    url_re = r'.*\(\"{1}(.*)\"\){1}'
    for row in range(1, np_sh.shape[0] + 1):
        try:
            processed_flag = 0 if np_sh[(row, 34)] == 'Нет' else 1           
            wom_flag = 1 if np_sh[row, 33] == 'WOM' else 0
            aggression_flag = 1 if np_sh[row, 26] == 'Агрессия' else 0
            author_url = re.sub(url_re, r'\1', np_sh[row, 9]) if np_sh[row, 9] else None
            source_url = re.sub(url_re, r'\1', np_sh[row, 12]) if np_sh[row, 12] else None
            logger.debug(f'Start create msg')
            message_dict = {
                "id_Сообщения": np_sh[row, 1],
                "Дата": np_sh[row, 0],
                "Заголовок": np_sh[row, 2],
                "Текст": np_sh[row, 3],
                "Url": re.sub(url_re, r'\1', np_sh[row, 5]),
                "Автор": np_sh[row, 8],
                "Url_автора": author_url,
                "Тип_автора": np_sh[row, 10],
                "Пол": np_sh[row, 13],
                "Возраст": np_sh[row, 14],
                "Тип_сообщения": np_sh[row, 7],
                "Источник": np_sh[row, 4],
                "Тип_источника": np_sh[row, 6],
                "Место_публикации": np_sh[row, 11],
                "Url_места_публикации": source_url,
                "Аудитория": np_sh[row, 15],
                "Комментариев": np_sh[row, 16],
                "Цитируемость": np_sh[row, 17],
                "Репостов": np_sh[row, 18],
                "Лайков": np_sh[row, 19],
                "Вовлеченность": np_sh[row, 20],	
                "Просмотров": np_sh[row, 21],	
                "Оценка": np_sh[row, 22],
                "Дублей": np_sh[row, 23],	
                "Тональность": np_sh[row, 24],	
                "Роль_объекта": np_sh[row, 25],	
                "Агрессия": aggression_flag,
                "Страна": np_sh[row, 27],	
                "Регион": np_sh[row, 28],	
                "Город": np_sh[row, 29],
                "Место": np_sh[row, 30],	
                "Адрес": np_sh[row, 31],	
                "Язык": np_sh[row, 32],	
                "WOM": wom_flag,	
                "Обработано": processed_flag,
            }
            message = Message(**message_dict)
            logger.debug(f"End create {message.id_Сообщения} msg")
            add_to_db(message)
            logger.info(f"Add {message.id_Сообщения} msg")
            try:
                msg_tags = []
                for column in range(35, max_col):
                    if np_sh[row, column]:
                        msg_tags.append(np_sh[row, column])
                add_tags_to_message(message.id_Сообщения, msg_tags)
            except BaseException as er:
                logger.error(er)
            logger.info(f"Add {message.id_Сообщения} tags msg")
        except BaseException as er:
            logger.error(er)
            continue


def run():
    '''Run a parser'''
    logger.add(
        "logs/debug.log",
        format="{time} {level} {message}",
        level="DEBUG",
        rotation='15 MB',
        compression='zip')
    np_sh = open_excel()
    parse_tags(np_sh)
    parse_messages(np_sh)
    close_session()
    