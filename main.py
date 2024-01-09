from urllib.request import Request, urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer
import pandas as pd
from math import nan
from datetime import date
import psycopg2
import time
from selenium import webdriver
import csv

driver = webdriver.Firefox()

def mineItemsOnPage(soup):
    pageitems=[]
    gridItems = soup.find_all("li", {"class": ['fops-item fops-item--on_offer','fops-item fops-item--new','fops-item fops-item--other','fops-item']})
    for gridItem in gridItems:
        nameElement = gridItem.find("h4", {"class": "fop-title"})
        if nameElement != None:
            name=nameElement.text
            if nameElement.has_attr('title'):
                title=nameElement['title']
            else:
                title=''
        else:
            name=''
            title=''
        
            

        PricePerUnitElement = gridItem.find("span", {"class": ["fop-price","fop-price price-offer"]})
        if PricePerUnitElement != None:
            PricePerUnit=PricePerUnitElement.text
        else:
            PricePerUnit=''

        
        PricePerMeasureElement = gridItem.find("span", {"class": "fop-unit-price"})
        if PricePerMeasureElement != None:
            PricePerMeasure=PricePerMeasureElement.text
        else:
            PricePerMeasure=''
        

        PromotionElement = gridItem.find("a", {"class": "fop-row-promo promotion-offer"})
        if PromotionElement != None:
            Promotion=PromotionElement.text
        else:
            Promotion=''
        
        itemList=[title,name,PricePerUnit,PricePerMeasure,Promotion]
        pageitems.append(itemList)
        print(itemList)
    return pageitems


def ExtractData(catName):
    items=[]
    url='https://groceries.morrisons.com/browse/'+catName+'?display=10000&sort=NAME_ASC'
    driver.get(url)
    time.sleep(10)
    total_height = int(driver.execute_script("return document.body.scrollHeight"))
    for i in range(1, total_height, 5):
        driver.execute_script("window.scrollTo(0, {});".format(i))
    time.sleep(10)
    html_page = (driver.page_source).encode('utf-8')
    soup = bs(html_page, 'html.parser')
    items = items + mineItemsOnPage(soup)
    time.sleep(5)
    fields=['name','Price Per Unit','Price Per Measure','Promotion']
    with open('Outfiles\\'+catName+'.csv', 'w',newline='', encoding="utf-8") as f:
    
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(items)


#ExtractData('meat-poultry-179549')
#ExtractData('fish-seafood-184367')
#ExtractData('fruit-veg-176738')
#ExtractData('fresh-176739')
#ExtractData('bakery-cakes-102210')
ExtractData('food-cupboard-102705')
#ExtractData('frozen-180331')
#ExtractData('drinks-103644')
#ExtractData('beer-wines-spirits-103120')
#ExtractData('household-102063')
#ExtractData('home-garden-166274')
#ExtractData('health-wellbeing-medicines-103497')
#ExtractData('toiletries-beauty-102838')
#ExtractData('baby-toddler-177598')
#ExtractData('toys-entertainment-166275')
#ExtractData('pet-shop-102207')
#ExtractData('free-from-175652')
#ExtractData('world-foods-182137')
