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
    product_skus = set()
    base_url += '?experienceName=default&Nao=%s'
    
   
    for page_num in range(0,1000):
        print(f"set lenght = {len(product_skus)}")
        url = base_url % (page_num*24)
        print(f"{url}")

        driver.get(url)
        
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(3)

        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        driver.close() # closing the webdriver

        prev_len = len(product_skus)

        father_meta = soup.find_all('div',"class:browse-search__pod col__6-12 col__6-12--xs col__4-12--sm col__4-12--md col__3-12--lg")
        meta = soup.find_all('meta',attrs={"data-prop":"productID"})


        for state in meta:
            product_skus.add(state['content'].split(".")[0])

        print(product_skus)


        if len(product_skus) == prev_len: break # this line is optional and can determine when you want to break
        

    return product_skus
  

print(load_dinamically("5yc1vZc3q0"))


def sku_finder(param):

    product_skus = set()
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'}
    
    base_url = redirect_link(param)
    base_url += '?experienceName=default&Nao=%s'

   
    for page_num in range(0,1000):
        print(f"set lenght = {len(product_skus)}")
        url = base_url % (page_num*24)
        print(f"{url}")

        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as url:
            
            soup = BeautifulSoup(url, "lxml")  
        res = soup.find_all('meta',attrs={"data-prop":"productID"})

        prev_len = len(product_skus)
        print(f"set lenght = {len(product_skus)}")
        for state in res:
            product_skus.add(state['content'].split(".")[0])
        if len(product_skus) == prev_len: break # this line is optional and can determine when you want to break

    return product_skus

# print(sku_finder("5yc1vZc3q0"))