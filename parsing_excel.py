from pprint import pprint
# import pandas as pd
import openpyxl as oxl
import re

file = 'MMH_RESPI_s_05.12.2022_13.04.2023-14.04.2023_643952c3ed42dd6e9d2b9572.xlsx'

wb = oxl.open(file)
sh = wb.worksheets[1]
sh.delete_cols(0)
sh.delete_rows(1, 5)

urls_msgs = []

url_re = r'.*\(\"{1}(.*)\"\){1}'

for row in range(2, 10):
    urls_msgs.append(re.sub(url_re, r'\1', sh[row][5].value))

pprint(urls_msgs)


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
