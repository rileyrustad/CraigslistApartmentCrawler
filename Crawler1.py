import pandas as pd
import numpy as np
from pandas import Series,DataFrame
from bs4 import BeautifulSoup
import requests
import time
import random
import datetime
unexplored_id_numbers=[]
data = {}
now = datetime.datetime.now()  
now_plus_seven = now + datetime.timedelta(days = 7)
#this function gets the newest apartment entries
#and appends them to our existing list of unexplored ID numbers
def NumberGetter(unexplored_id_numbers,data):
    #get html information    
    url = 'http://portland.craigslist.org/search/mlt/apa'
    result = requests.get(url)
    c = result.content
    soup = BeautifulSoup(c,'lxml')

    #organize it down to just the ID numbers
    summary = soup.find("div",{'class':'content'})
    rows = summary.find_all("p",{'class':'row'})
    data = {}
    new_id_numbers = []
    
    for i in rows:
        r = str(i)
        new_id_numbers.append(r[25:35])
    for number in new_id_numbers:
        if number not in data:
            unexplored_id_numbers.append(number)
        
    return unexplored_id_numbers 

def InfoGetter(id_number,data):
    url = 'https://portland.craigslist.org/mlt/apa'+'/'+id_number+'.html'
    result = requests.get(url)
    c = result.content
    soup = BeautifulSoup(c,'lxml')
    #get the price
    price = GetPrice(soup)   
    #get the listed attributes    
    attributes = GetAttributes(soup)
    #get the number of beds and baths
    bedbath = [GetBedBath(soup)]
    if len(bedbath) == 2:
        bed,bath = bedbath[0],bedbath[1]
    elif len(bedbath) == 1:
        bed,bath = bedbath[0],np.nan
    else:
        bed,bath = np.nan,np.nan
    data[id_number]=[price,bed,bath,attributes]
    return data
    
def GetAttributes(soup):    
    summary = soup.find("div",{'class':'mapAndAttrs'})
    if summary == None:
        return np.nan
    else:    
        summary2 = summary.find_all("span")
        summary2
        attributes = []
        for i in summary2:
            text = i.find(text=True)
            attributes.append(text)
    return attributes[0:]
    
def GetBedBath(soup):
    summary = soup.find("div",{'class':'mapAndAttrs'})
    if summary == None:
        return np.nan
    else: 
        summary2 = summary.find_all("b")    
        text = summary2[0].find(text=True)
        if len(summary2)>1:
            text2 = summary2[1].find(text=True)
            return text, text2
        else:
            return text
    
def GetPrice(soup):
    summary = soup.find("span",{'class':'price'})
    if summary == None:
        return np.nan
    else: 
        text = summary.find(text=True)
    return text    

#def FinalCrawler(unexplored_id_numbers,data):
#    unexplored_id_numbers = NumberGetter(unexplored_id_numbers)
#    time.sleep(5)
#    while len(unexplored_id_numbers) > 0:
#        time.sleep(5)
#        id_number = unexplored_id_numbers.pop(0)
#        data = InfoGetter(id_number,data)
#    while 

def TestCrawler(unexplored_id_numbers,data, now):
    unexplored_id_numbers = NumberGetter(unexplored_id_numbers,data)
    time.sleep(5)
    counter = 4
    while counter > 0:
        time.sleep(random.randrange(5, 10))
        id_number = unexplored_id_numbers.pop(0)
        data = InfoGetter(id_number,data)
        counter -= 1
#    while datetime.datetime.now() < now_plus_seven:
#        time.sleep(900)
#        TestCrawler(unexplored_id_numbers,data, now):
    return data
    
#def FinalCrawlerShell():
#    unexplored_id_numbers=[]
#    data = {}
#    now = datetime.datetime.now()  
#    now_plus_seven = now + datetime.timedelta(days = 7)
#    data = FinalCrawler(unexplored_id_numbers,data, now):
        
def TestCrawlerShell():
    unexplored_id_numbers=[]
    data = {}
    now = datetime.datetime.now()  
    now_plus_seven = now + datetime.timedelta(days = 7)
    data = TestCrawler(unexplored_id_numbers,data, now)
    return data
    
x = TestCrawlerShell()
print x

        
pandadata = pd.DataFrame(x)
print pandadata
