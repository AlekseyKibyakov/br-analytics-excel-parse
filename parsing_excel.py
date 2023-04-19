from datetime import datetime
import db_interaction as db
import openpyxl as oxl
import re
from progress.bar import IncrementalBar

from models import Message, Tag

file = 'MMH_RESPI_s_05.12.2022_13.04.2023-14.04.2023_643952c3ed42dd6e9d2b9572.xlsx'

wb = oxl.open(file)
sh = wb.worksheets[1]
sh.delete_cols(0)
sh.delete_rows(1, 5)

urls_msgs = []

url_re = r'.*\(\"{1}(.*)\"\){1}'

bar = IncrementalBar('Countdown', max=sh.max_row + 1)

# sh.max_row + 1
tags = {}
start_time = datetime.now()
for column in range(35, sh.max_column):
    tags[str(column)] = sh[1][column].value
    tag = Tag(Название = sh[1][column].value)
    db.add_to_db(tag)

# print(tags)

for row in range(2, sh.max_row + 1):
    # try:
        if sh[row][34].value == 'Нет':
            sh[row][34].value = 0
        else:
            sh[row][34].value = 1
        
        if sh[row][33].value == 'WOM':
            sh[row][33].value = 1
        else:
            sh[row][33].value = 0
        
        if sh[row][26].value == 'Агрессия':
            sh[row][26].value = 1
        else:
            sh[row][26].value = 0
        
        message = Message(
            id_Сообщения = sh[row][1].value,
            Дата = sh[row][0].value,
            Заголовок = sh[row][2].value,
            Текст = sh[row][3].value,
            Url = re.sub(url_re, r'\1', sh[row][5].value),
            Автор = sh[row][8].value,
            Url_автора = sh[row][9].value,
            Тип_автора = sh[row][10].value,
            Пол = sh[row][13].value,
            Возраст = sh[row][14].value,
            Тип_сообщения = sh[row][7].value,
            Источник = sh[row][4].value,
            Тип_источника = sh[row][6].value,
            Место_публикации = sh[row][11].value,
            Url_места_публикации = sh[row][12].value,
            Аудитория = sh[row][15].value,
            Комментариев = sh[row][16].value,
            Цитируемость = sh[row][17].value,
            Репостов = sh[row][18].value,
            Лайков = sh[row][19].value,
            Вовлеченность = sh[row][20].value,	
            Просмотров = sh[row][21].value,	
            Оценка = sh[row][22].value,
            Дублей = sh[row][23].value,	
            Тональность = sh[row][24].value,	
            Роль_объекта = sh[row][25].value,	
            Агрессия = sh[row][26].value,
            Страна = sh[row][27].value,	
            Регион = sh[row][28].value,	
            Город = sh[row][29].value,
            Место = sh[row][30].value,	
            Адрес = sh[row][31].value,	
            Язык = sh[row][32].value,	
            WOM = sh[row][33].value,	
            Обработано = sh[row][34].value
        )
        
        db.add_to_db(message)
        
        msg_tags = []
        for column in range(35, sh.max_column):
            if sh[row][column].value:
                msg_tags.append(sh[row][column].value)
        
        db.add_tags_to_message(message.id_Сообщения, msg_tags)
        bar.next()
    # except:
    #     continue

elapsed_time = datetime.now() - start_time

db.session.close()
print(elapsed_time)
bar.finish()
# message_dict['tags'] = []
    
    # for column in range(35, sh.max_column):
    #     if sh[row][column]:
    #         message_dict['tags'].append(sh[row][column].value)
    
    # pprint(message_dict)
    
        
    

    # pprint(message_dict)
    # message_dict.setdefault('url', re.sub(url_re, r'\1', sh[row][5].value))




# df_mentions = pd.read_excel(file, sheet_name='Упоминания', engine='openpyxl')

# df_mentions = df_mentions.drop(columns='Unnamed: 0')

# titles_list = df_mentions.iloc[4].values.copy()

# df_mentions = df_mentions.drop([0, 1, 2, 3, 4])

# df_mentions.columns = titles_list

# df_mentions.reset_index(drop=True, inplace=True)

# df_mentions.to_csv('test.csv', encoding='utf8')

# urls = df_mentions.iloc[:, 4]

# print(urls)

# # Сброс ограничений на количество выводимых рядов
# pd.set_option('display.max_rows', 50)
 
# # Сброс ограничений на число столбцов
# pd.set_option('display.max_columns', None)
 
# # Сброс ограничений на количество символов в записи
# pd.set_option('display.max_colwidth', None)
