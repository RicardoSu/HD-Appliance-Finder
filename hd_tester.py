import requests,json,re,urllib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


def redirect_link(param):
    res = urllib.request.urlopen(f'https://www.homedepot.com/b/N-{param}')
    finalurl = res.geturl()
    return finalurl



def load_dinamically(param):

    base_url = redirect_link(param)
    print(base_url)
    
    
    driver = webdriver.Chrome('./chromedriver')
    tags_dict = dict() 
    product_skus = set()
    base_url += '?experienceName=default&Nao=%s'
    
   
    for page_num in range(0,1000):
        url = base_url % (page_num*24)

        driver.get(url)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(4)

        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")

        father_meta = soup.find_all('div',"class:browse-search__pod col__6-12 col__6-12--xs col__4-12--sm col__4-12--md col__3-12--lg")
        meta = soup.find_all('meta',attrs={"data-prop":"productID"})

        try:
            if meta in father_meta:
                return meta
        except AttributeError:
            print("meta is not a child of father")

        prev_len = len(product_skus)
        for state in meta:
            product_skus.add(state['content'].split(".")[0])

        if len(product_skus) == prev_len: break # this line is optional and can determine when you want to break
    
    driver.close() # closing the webdriver
    print(f"{len(product_skus)} SKU'S")
    return product_skus
  

print(load_dinamically("5yc1vZc3ns"))


def sku_finder(param):

    product_skus = set()
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'}
    
    base_url = redirect_link(param)
    base_url += '?experienceName=default&Nao=%s'

   
    for page_num in range(0,1000):
        url = base_url % (page_num*24)

        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as url:
            
            soup = BeautifulSoup(url, "lxml")  
        res = soup.find_all('meta',attrs={"data-prop":"productID"})

        prev_len = len(product_skus)

        for state in res:
            product_skus.add(state['content'].split(".")[0])
        if len(product_skus) == prev_len: break # this line is optional and can determine when you want to break

    return product_skus

# print(sku_finder("5yc1vZc3q0"))