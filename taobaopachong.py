import pymongo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
from urllib.parse import quote
from multiprocessing import *
import multiprocessing as mp
import os
import sys
import tesserocr
from PIL import Image
from xlwt import *
from xlrd import *
import requests

PROXY_POOL_URL = 'http://localhost:5000/get'

USERNAME='自己的微博账号'
USERPASSWORD='自己的微博密码'

MONGO_URL = 'localhost'
MONGO_DB = 'taobao爬虫'
MONGO_COLLECTION = 'products'

KEYWORD = '手机'

MAX_PAGE = 200

SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']

# browser = webdriver.Chrome()
# browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
browser = webdriver.Chrome(options=options)

wait = WebDriverWait(browser, 10)
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

global sheettitle, row, ws, w,all_product
w = Workbook(encoding='utf-8')
ws = w.add_sheet('taobaoxinxi',cell_overwrite_ok=True)
row=1
sheettitle = ['image', 'price', 'deal', 'title', 'shop', 'location']
all_product=[]
def login_page():
        """
        模拟登陆
        """
        url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
        browser.get(url)
        browser.maximize_window()
        loginway=wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_QRCodeLogin > div.login-links > a.forget-pwd.J_Quick2Static')))
        loginway.click()
        loginweibo = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_OtherLogin > a.weibo-login')))
        loginweibo.click()
        #账号密码填写
        name=browser.find_element_by_name('username')
        password=browser.find_element_by_name('password')
        name.send_keys(USERNAME)
        password.send_keys(USERPASSWORD)
        #点击登录按钮
        loginww=browser.find_element_by_xpath('//*[@class="btn_tip"]/a/span')
        loginww.click()
        # #解析微博登录验证码
        # weibover=browser.page_source
        # doct=pq(weibover)
        # img=doct()
        #     find_element_by_xpath('//*[@id="pl_login_logged"]/div/div[4]/div/a[1]/img')



def index_page(page):
    """
    抓取索引页
    :param page: 页码
    """
    print('正在爬取第', page, '页')
    try:
        if page > 1:
            input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
            submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
            input.clear()
            input.send_keys(page)
            submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
        get_products(page)
    except TimeoutException:
        index_page(page)


def get_products(row):
    """
    处理滑块验证码
    提取商品数据
    """
    # slideblock=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'')))

    global all_product,product
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('data-src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)
        save_to_excel(product)

def save_to_excel(result):
    """
    保存至excel
    :param result: 结果
    #"""
    # try:
    global row
    for i in range(6):
        ws.write(row, i, result[sheettitle[i]])
        w.save('H:/taobao1.xls')
    row += 1
    # except Exception:
    # print('存储到EXCEL失败')


def main():
    """
    遍历每一页
    """
    login_page()
    """
    创建表格表头
    """

    for i in range(0,int(len(sheettitle))):
        ws.write(0, i, sheettitle[i])

    for i in range(36, MAX_PAGE + 1):
        index_page(i)
    browser.close()


if __name__ == '__main__':
    main()

