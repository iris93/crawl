# coding:utf-8

import tabula
import sys

path = sys.path[0]+"\\"+"W020180815546072521781.pdf"
# df = tabula.read_pdf(path,encoding="gbk" ,pages='1')
# # print(df)
# tabula.convert_into(path, "output.json", output_format="json")
# # for indexs in df.index:
# #     print indexs
# #     print(df.loc[indexs].values)
# print df.loc[17].values

import pdfplumber

pdf = pdfplumber.open('./ccb_funds/W020180815546072521781.pdf')

p0 = pdf.pages[0]#注意此处的pages是一个列表，索引是从0开始的

table = p0.extract_table()

import pandas as pd

df = pd.DataFrame(table[1:], columns=table[0])
df.to_csv('result.csv',encoding='utf-8')
# print df