# 淘宝网手机商品销量爬取和分析
> 手机数据大调查！  

## 概况  

国内手机市场愈演愈烈，想要探究手机商铺分布以及销售情况，爬取内容为淘宝搜索手机出现的100页商品信息，包括店铺标题，店铺所在地以及销量等等。
因为淘宝网反爬措施，需要模拟登陆进行爬取，且时间频次不宜过高，抵制频繁无限制爬取，现用python+selenium库进行爬取，得到100页商品信息，共4000多条（样本比较少，本项目仅作简要分析）

## 前言  
###  对数据进行如下几样分析：
1. 对商品标题进行文本分析 词云可视化
2. 不同关键词word对应的sales的统计分析
3. 商品的价格分布情况分析
4. 商品的销量分布情况分析
5. 不同价格区间的商品的平均销量分布
6. 商品价格对销量的影响分析
7. 不同省份或城市的商品数量分布
8. 不同省份的商品平均销量分布
### 总体步骤：
1. 数据采集：Python爬取淘宝网商品数据
2. 对数据进行清洗和处理 
3. 文本分析：jieba分词、wordcloud可视化
4. 数据柱形图可视化 barh
5. 数据直方图可视化 hist
6. 数据散点图可视化 scatter
## 缺失值分析
对数据进行清洗处理，得到缺失值分析图：
![phone_Missing value Analysis](https://github.com/cjhayes16/taobao_spider/blob/master/img/0.png)
## 标题  

对店铺标题进行分词统计词频，清理数据后对 top30 生成条形图  

![titles_word_top_30](https://github.com/cjhayes16/taobao_spider/blob/master/img/1.png)  

来个词云  

![titles_wordcloud](https://github.com/cjhayes16/taobao_spider/blob/master/img/2.png)  

## 销量  

### 商品的价格分布情况:

![price_distribution](https://github.com/cjhayes16/taobao_spider/blob/master/img/3.png) 
### 商品的销量分布情况:
![sales_distribution](https://github.com/cjhayes16/taobao_spider/blob/master/img/4.png) 
### 不同价格区间的商品的平均销量分布:
![price_mean_sales](https://github.com/cjhayes16/taobao_spider/blob/master/img/5.png) 
### 商品价格对销量的影响:
![The_Impact_of_Price_on_Sales](https://github.com/cjhayes16/taobao_spider/blob/master/img/6.png) 
### 不同省份的商品数量分布:
![num_different_provinces](https://github.com/cjhayes16/taobao_spider/blob/master/img/7.png) 
### 不同省份的商品平均销量分布:
![mean_sales_different_provinces](https://github.com/cjhayes16/taobao_spider/blob/master/img/8.png)

# 本项目仅供学习交流所用，严禁用于商业用途！
