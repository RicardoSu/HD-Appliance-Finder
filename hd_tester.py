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
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'}
    

    
    base_url += '?experienceName=default&Nao=%s'
    driver.get(base_url)
    

    html = driver.page_source
   
    for page_num in range(0,1000):
        print(f"set lenght = {len(product_skus)}")
        url = base_url % (page_num*24)
        print(f"{url}")

# soup = BeautifulSoup(html, "html.parser")
# all_divs = soup.find('div', {'id' : 'nameSearch'})
# job_profiles = all_divs.find_all('a')


        req = urllib.request.Request(html, headers=headers)
        with urllib.request.urlopen(req) as url:
            
            soup = BeautifulSoup(url, "lxml")  
        res = soup.find_all('meta',attrs={"data-prop":"productID"})

        prev_len = len(product_skus)
        print(f"set lenght = {len(product_skus)}")
        for state in res:
            product_skus.add(state['content'].split(".")[0])
        if len(product_skus) == prev_len: break # this line is optional and can determine when you want to break

    return product_skus
  
    driver.close() # closing the webdriver


load_dinamically("5yc1vZc3q0")


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