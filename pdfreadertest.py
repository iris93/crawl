# coding:utf-8

import tabula
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# path = sys.path[0]+"\\"+"W020180815546072521781.pdf"
# df = tabula.read_pdf(path,encoding="gbk" ,pages='1')
# # print(df)
# tabula.convert_into(path, "output.json", output_format="json")
# # for indexs in df.index:
# #     print indexs
# #     print(df.loc[indexs].values)
# print df.loc[17].values

import pdfplumber
import pandas as pd

# pdf = pdfplumber.open('./abcpdf/P020180816442262220769.pdf')
pdf = pdfplumber.open('./abcpdf/P020180820677094177172.pdf')
# pdf = pdfplumber.open('./abcpdf/P020180821493413535312.pdf')
sys_encoding = sys.getfilesystemencoding()

def printcn(msg):
    print(msg.decode('utf-8').encode(sys_encoding))
def getScale(pdf):
    p0 = pdf.pages[1:3]#注意此处的pages是一个列表，索引是从0开始的
    for i in range(len(p0)):
        table = p0[i].extract_tables()
        for item in table:
            for subitem in item:
                if u'产品认购规模' in subitem:
                    print "found"
                    p=subitem.index(u'产品认购规模')
                    printcn(subitem[p+1])
                    return subitem[p+1]
                else:print "not found"
    return "not found"
result = getScale(pdf)
printcn(result)