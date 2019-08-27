import pymongo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
from urllib.parse import quote
import os
import sys
import tesserocr
from PIL import Image

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

def login_page():
        """
        模拟登陆
        """
        url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
        browser.get(url)
        loginway=wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_QRCodeLogin > div.login-links > a.forget-pwd.J_Quick2Static')))
        loginway.click()
        loginweibo = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_OtherLogin > a.weibo-login')))
        loginweibo.click()
        name=browser.find_element_by_name('username')
        password=browser.find_element_by_name('password')
        name.send_keys(USERNAME)
        password.send_keys(USERPASSWORD)
        loginww=browser.find_element_by_xpath('//*[@class="btn_tip"]/a/span')
        loginww.click()

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
        get_products()
    except TimeoutException:
        index_page(page)


def get_products():
    """
    提取商品数据
    """
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
        save_to_mongo(product)


def save_to_mongo(result):
    """
    保存至MongoDB
    :param result: 结果
    """
    try:
        if db[MONGO_COLLECTION].insert(result):
            print('存储到MongoDB成功')
    except Exception:
        print('存储到MongoDB失败')


def main():
    """
    遍历每一页
    """
    login_page()
    for i in range(1, MAX_PAGE + 1):
        index_page(i)
    browser.close()


if __name__ == '__main__':
    main()