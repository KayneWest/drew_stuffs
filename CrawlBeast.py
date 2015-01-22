from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import pandas as pd
from bs4 import BeautifulSoup
import re
import random
import datetime
import sys

html_escape_table = {
    "&amp;": "&",
    "&quot;":'"',
    "&apos;":"'",
    "&gt;":">",
     "&lt;":"<",
    }

def html_escape(text):
    """Produce entities within text."""
    return " ".join(html_escape_table.get(c,c) for c in text.split())

def log(msg):
    print("{} {}".format(str(datetime.datetime.now()), msg))

def removeNonAscii(s): 
    return "".join(filter(lambda x: ord(x)<128, s))

class GetSalesLists(object):
    def __init__(self):
        self.driver=webdriver.PhantomJS()
        self.company_names=[]

    def grocery(self):
        log("grabbing initial 'Grocery' page")
        self.grocery_html=[]
        self.driver.get('http://www.yelp.com/chicago')
        blue=self.driver.find_elements_by_css_selector('input#find_desc')[0]
        blue.send_keys('grocery')
        time.sleep(2)
        blue.send_keys(u'\ue015')
        time.sleep(2)
        blue.send_keys(u'\ue015')
        time.sleep(2)
        blue.send_keys(u'\ue007')
        time.sleep(10)
        self.grocery_html.append(self.driver.page_source)

        for i in range(10,200,10):
            num=random.randint(5,10)
            print 'waiting for '+ str(num)+' seconds'
            time.sleep(num)
            log('getting another link')
            link="http://www.yelp.com/search?find_desc=Grocery&find_loc=Chicago%2C+IL&start="+str(i)
            self.driver.get(link)
            self.grocery_html.append(self.driver.page_source)


    def get_names(self):
        for html in self.grocery_html:
            matches=re.findall(r'data-hovercard-id.*</a>',html)
            for match in matches:
                item=html_escape(removeNonAscii(re.findall(r'>.*</a>',match)[0][1:-4]))
                self.company_names.append(item)
        self.company_names=set(self.company_names)

    def list_names(self,argv):
        """ need to list a file name """
        print self.company_names
        with open('saleslist.txt','wb') as f:
            for company in self.company_names:
                f.write(company+'\t')

def main(argv):
    g=GetSalesLists()
    g.grocery()
    g.get_names()
    g.list_names(argv)

if __name__ == '__main__':
    main(sys.argv[1])
