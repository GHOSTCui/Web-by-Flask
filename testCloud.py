# -*- codeing = utf-8 -*-
# @Project: douban_flask
# @Package
# @Description: TODO
# @author : Ghost
# @date Date : 2021年08月12日 5:27 下午


import jieba        # 分词
from matplotlib import pyplot as plt        # 绘图，数据可视化
from wordcloud import WordCloud         # 词云
from PIL import Image               # 图片处理
import numpy as np               # 矩阵运算
import sqlite3              # 数据库

con = sqlite3.connect('movie.db')
cur = con.cursor()
sql = "select Inq from movieTop250"
data = cur.execute(sql)
text = ""
for item in data:
    text = text + item[0]
# print(text)
cur.close()
con.close()

# 分词
cut = jieba.cut(text)
string = ' '.join(cut)
# print(len(string))



img = Image.open(r'/Users/ghost7/Documents/Study/PyProjects/douban_flask/static/assets/img/tree.jpeg')
img_array = np.array(img)       # 将图片转化为数组
wc = WordCloud(
    background_color = 'white',
    mask = img_array,
    font_path="PingFang.ttc"

)
wc.generate_from_text(string)

# 绘制图片
fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')         # 是否显示坐标轴

# plt.show()          # 显示生成的词云图片
plt.savefig(r'/Users/ghost7/Desktop/word.jpg',dpi=500)          # 保存图片


