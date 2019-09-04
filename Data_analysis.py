import re
import time
import requests
import pandas as pd
from retrying import retry
from concurrent.futures import ThreadPoolExecutor
import random

data=pd.read_excel('H:/data.xls')
'''
三、数据挖掘与分析：

【1】. 对 title 列标题进行文本分析：
   使用结巴分词器，安装模块pip install jieba
'''
titles = data.title.values.tolist()  # 转为list

# 对每个标题进行分词：  使用lcut函数
import jieba

title_s = []
for line in titles:
    title_cut = jieba.lcut(line)
    title_s.append(title_cut)

'''
对 title_s（list of list 格式）中的每个list的元素（str）进行过滤 剔除不需要的词语，
即 把停用词表stopwords中有的词语都剔除掉：
'''

# 导入停用词表：
stopwords = pd.read_excel('H:/stopwords.xlsx')
stopwords = stopwords.stopword.values.tolist()

# 剔除停用词：
title_clean = []
for line in title_s:
    line_clean = []
    for word in line:
        if word not in stopwords:
            line_clean.append(word)
    title_clean.append(line_clean)

'''
因为下面要统计每个词语的个数，所以 为了准确性 这里对过滤后的数据 title_clean 中的每个list的元素进行去重，
即 每个标题被分割后的词语唯一。 
'''
title_clean_dist = []
for line in title_clean:
    line_dist = []
    for word in line:
        if word not in line_dist:
            line_dist.append(word)
    title_clean_dist.append(line_dist)

# 将 title_clean_dist 转化为一个list: allwords_clean_dist
allwords_clean_dist = []
for line in title_clean_dist:
    for word in line:
        allwords_clean_dist.append(word)

# 把列表 allwords_clean_dist 转为数据框：
df_allwords_clean_dist = pd.DataFrame({'allwords': allwords_clean_dist})

# 对过滤_去重的词语 进行分类汇总：
word_count = df_allwords_clean_dist.allwords.value_counts().reset_index()
word_count.columns = ['word', 'count']  # 添加列名

'''
观察 word_count 表中的词语，发现jieba默认的词典 无法满足需求： 
有的词语（如 老人机、全面屏等）却被cut，这里根据需求对词典加入新词
（也可以直接在词典dict.txt里面增删，然后载入修改过的dict.txt）
'''
add_words = pd.read_excel('add_words.xlsx')  # 导入整理好的待添加词语

# 添加词语：
for w in add_words.word:
    jieba.add_word(w, freq=1000)

# =======================================================================
# 注：再将上面的 分词_过滤_去重_汇总 等代码执行一遍，得到新的 word_count表
# =======================================================================

word_count.to_excel('H:/word_count.xlsx', index=False)    #导出数据




'''
以上注释：
123.jpg 是透明背景图 将该图放在Python的项目路径下！
".H:\python3_project\SIMLI.TTF"   设置字体
background_color   默认是黑色 这里设置成白色
head(100)   取前100个词进行可视化！ 
max_font_size　 字体最大字号 
interpolation='bilinear'  图优化   
"off"   去除边框
'''

'''
分析结论：
1. 通讯公司中网通占比很高；
2. 从手机种类看：全面屏智能手机占比很高，比老年机多；
3. 从手机品牌来看：华为最多，华为子品牌荣耀次之，其他风格排名依次是苹果、vivo、xiaomi、三星等；
4. 从手机功能特性来看：超长待机占比最高、能玩游戏次之，指纹识别第三，其他还有双屏，曲面，四摄等等；
'''

'''
【2】. 不同关键词word对应的sales之和的统计分析： 
  （说明：例如 词语 ‘老人机’，则统计商品标题中含有‘老人机’一词的商品的销量之和，即求出具有‘老人机’特性的商品销量之和）
   代码如下：
'''
import numpy as np

w_s_sum = []
for w in word_count.word:
    i = 0
    s_list = []
    for t in title_clean_dist:
        if w in t:
            s_list.append(data.sales[i])
        i += 1
    w_s_sum.append(sum(s_list))  # list求和

df_w_s_sum = pd.DataFrame({'w_s_sum': w_s_sum})

# 把 word_count 与对应的 df_w_s_sum 合并为一个表：
df_word_sum = pd.concat([word_count, df_w_s_sum], axis=1, ignore_index=True)
df_word_sum.columns = ['word', 'count', 'w_s_sum']  # 添加列名
df_word_sum.to_excel('H:/word_sum.xls')

'''
对表df_word_sum 中的 word 和 w_s_sum 两列数据进行可视化： 见下<图3>
（本例中取销量排名前30的词语进行绘图）
'''
df_word_sum.sort_values('w_s_sum', inplace=True, ascending=True)  # 升序
df_w_s = df_word_sum.tail(30)  # 取最大的30行数据

import matplotlib
from matplotlib import pyplot as plt

font = {'family': 'SimHei'}  # 设置字体
matplotlib.rc('font', **font)

index = np.arange(df_w_s.word.size)
plt.figure(figsize=(6, 12))
plt.barh(index, df_w_s.w_s_sum, color='green', align='center', alpha=0.8)
plt.yticks(index, df_w_s.word, fontsize=11)

# 添加数据标签：
for y, x in zip(index, df_w_s.w_s_sum):
    plt.text(x, y, '%.0f' % x, ha='left', va='center', fontsize=11)
data['price'] = data.price.apply(lambda x: x.split('¥')[1])
data['price'] = data.price.apply(lambda x: x.split('.')[0])
data['price']=data.price.astype('int')
data_p = data[data['price'] < 20000]

plt.figure(figsize=(7, 5))
plt.hist(data_p['price'], bins=50, color='green')  # 分为15组
plt.xlabel('价格', fontsize=12)
plt.ylabel('商品数量', fontsize=12)
plt.title('不同价格对应的商品数量分布', fontsize=15)


data_s = data[data['sales'] > 50]
print('销量50以上的商品占比: %.3f' % (len(data_s) / len(data)))

plt.figure(figsize=(7, 5))
plt.hist(data_s['sales'],bins=15, color='green',align='mid')  # 分为15组
plt.xlabel('销量', fontsize=12)
plt.ylabel('商品数量', fontsize=12)
plt.title('不同销量对应的商品数量分布', fontsize=15)

data['group'] = pd.qcut(data.price, 12)
df_group = data.group.value_counts().reset_index()  # 生成数据框并重设索引

# 以group列进行分类求sales的均值：
df_s_g = data[['sales', 'group']].groupby('group').mean().reset_index()

# 绘柱形图：
index = np.arange(df_s_g.group.size)
plt.figure(figsize=(8, 4))
plt.bar(index, df_s_g.sales, color='green')
plt.xticks(index, df_s_g.group, fontsize=11, rotation=30)
plt.xlabel('Group')
plt.ylabel('平均销量')
plt.title('不同价格区间的商品的平均销量')


fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(data_p['price'], data_p['sales'], color='green')
ax.set_xlabel('价格')
ax.set_ylabel('销量')
ax.set_title('商品价格对销量的影响', fontsize=14)


data['GMV'] = data['price'] * data['sales']

import seaborn as sns

sns.regplot(x="price", y='GMV', data=data, color='green')

plt.figure(figsize=(8, 4))
data.province.value_counts().plot(kind='bar', color='green')
plt.xticks(rotation=0)
plt.xlabel('省份')
plt.ylabel('数量')
plt.title('不同省份的商品数量分布')
plt.show()


pro_sales = data.pivot_table(index='province', values='sales', aggfunc=np.mean)  # 分类求均值
pro_sales.sort_values('sales', inplace=True, ascending=False)  # 排序
pro_sales = pro_sales.reset_index()  # 重设索引

index = np.arange(pro_sales.sales.size)
plt.figure(figsize=(8, 4))
plt.bar(index, pro_sales.sales, color='green')
plt.xticks(index, pro_sales.province, fontsize=11, rotation=0)
plt.xlabel('province')
plt.ylabel('平均销量')
plt.title('不同省份的商品平均销量分布')
plt.show()

pro_sales.to_excel('H:/pro_sales.xlsx', index=False)  # 导出数据 并绘制热力型地图
