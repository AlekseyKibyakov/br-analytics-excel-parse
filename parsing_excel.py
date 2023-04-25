from collections import Counter
from datetime import datetime
from itertools import count
from db_interaction import add_to_db, add_tags_to_message, session
import openpyxl as oxl
import re
from progress.bar import IncrementalBar
# from loguru import logger
from models import Message, Tag
import numpy as np
# logger.add("debug.log", format="{time} {level} {message}", level="DEBUG")

def run():
    file = 'report.xlsx'

    wb = oxl.load_workbook(file, read_only=True)
    sh = wb.worksheets[1]
    # np_sh.delete_cols(0)
    # np_sh.delete_rows(1, 5)

    np_sh = np.array([[i for i in j] for j in sh.iter_rows(min_row=6, min_col=2, values_only=True)])
    
    url_re = r'.*\(\"{1}(.*)\"\){1}'

    bar = IncrementalBar('Countdown', max=np_sh.shape[0] + 1)

    start_time = datetime.now()
    max_col = np_sh.shape[1] + 1
    for column in range(35, max_col-1):
        # try:
            tag = Tag(Название = np_sh[0, column])
            add_to_db(tag)
            # logger.info(f"Add {tag.Название} tag")
        # except:
            # session.rollback()
            # continue
    
    
    for row in range(1, np_sh.shape[0] + 1):
        try:
            processed_flag = 0 if np_sh[(row, 34)] == 'Нет' else 1
            
            wom_flag = 1 if np_sh[row, 33] == 'WOM' else 0

            aggression_flag = 1 if np_sh[row, 26] == 'Агрессия' else 0
            
            author_url = re.sub(url_re, r'\1', np_sh[row, 9]) if np_sh[row, 9] else None

            source_url = re.sub(url_re, r'\1', np_sh[row, 12]) if np_sh[row, 12] else None
            # logger.debug(f'Start create msg')
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
            # logger.debug(f"End create {message.id_Сообщения} msg")
            add_to_db(message)
            # logger.info(f"Add {message.id_Сообщения} msg")
            msg_tags = []
            for column in range(35, max_col-1):
                if np_sh[row, column]:
                    msg_tags.append(np_sh[row, column])
            
            add_tags_to_message(message.id_Сообщения, msg_tags)
            # logger.info(f"Add {message.id_Сообщения} tags msg")
            bar.next()
        except:
            continue

    elapsed_time = datetime.now() - start_time

    session.close()
    print('\n')
    wb.close()
    print(elapsed_time)
    bar.finish() 
