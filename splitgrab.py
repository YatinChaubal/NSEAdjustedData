__author__ = 'Yatin'

from BeautifulSoup import BeautifulSoup
import re
import mechanize
import cookielib
from urlparse import urlparse
from os.path import splitext, basename, sys
import os
import datetime
import time
import urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class GrabSplitMecahnize:
    def __init__(self,
        weblink="http://www.sharekhan.com/stock-market/equity/company-statistics/statistics-details/stock-splits/18/MarketInfoSplits.htm"):
        self.baseweblink=weblink
        self.browser = mechanize.Browser()
        self.browser.set_handle_robots(False)
        # Cookie Jar
        cj = cookielib.LWPCookieJar()
        self.browser.set_cookiejar(cj)
        self.browser.addheaders = [('user-agent', '   Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3'),
            ('accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]
        self.csvfile=open('split.csv','w')


    def GetSplits(self):

        r = self.browser.open(self.baseweblink)
        for f in self.browser.forms():
            print f
        #form = self.browser.select_form(name='aspnetForm')
        self.browser[eventTarget] = 'ctl00$Content$MarketInfoSplits1$gvSplits'
        self.browser[eventArgument] = 'Page$7'
        response1 = self.browser.submit()
        html = (self.browser.open(self.baseweblink)).read()
        soup = BeautifulSoup(html)
        table = soup.find( "table", {"id":"ctl00_Content_MarketInfoSplits1_gvSplits"} )
        for row in table.findAll("tr"):
            cols = row.findAll('td')
            csvout=""
            for td in cols:
                if td.text !="":
                    csvout=csvout+","+td.text
            self.csvfile.write(csvout)

    def __del__(self):
        self.csvfile.close()



class GrabSplitSelenium:
    def __init__(self,
        weblink="http://www.sharekhan.com/stock-market/equity/company-statistics/statistics-details/stock-splits/18/MarketInfoSplits.htm"):
        self.weblink=weblink
        self.driver = webdriver.PhantomJS(executable_path='E:\phantomjs-1.9.8-windows\phantomjs.exe')
        #self.driver = webdriver.Firefox()
        self.driver.set_window_size(1400, 1000)
        self.driver.implicitly_wait(10)
        self.base_url = "http://www.sharekhan.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.csvfile=open('split.csv','w')
        self.csvfile.write("Company,CMP,Old Face Value,New Face Value,Record Date,Split Date,Implemented\n")


    def GetSplits(self,html):

        soup = BeautifulSoup(html)
        maxpage=0
        table = soup.find( "table", {"id":"ctl00_Content_MarketInfoSplits1_gvSplits"} )
        cvsout = ""
        for row in table.findAll("tr"):

            if row.get('class'):
                #print "class"
                continue
            cols = row.findAll('td')
            csvout=""
            for td in cols:
                #csvout=""
                if str(td)[13:23] == "javascript":
                    #print "found javascript"

                    maxpage=td.text
                    continue
                #print "finding one",str(td)[0:11]
                if "<td><span>1" == str(td)[0:11]:
                    continue;
                #print "TD=",td
                if td.text !="":
                    if csvout =="":
                        csvout=str(td.text)
                    else:
                        csvout=csvout+","+td.text
            if len(csvout) > 0:
                self.csvfile.write(csvout+"\n")
            #print csvout
        return maxpage

    def selectyear(self,year,driver):
        driver.find_element_by_id("ctl00_Content_MarketInfoSplits1_Year").click()
        driver.find_element_by_id("ctl00_Content_MarketInfoSplits1_Year").click()
        #Select(driver.find_element_by_id("ctl00_Content_MarketInfoSplits1_Year")).select_by_visible_text(year)
        #Select(driver.find_element_by_id("ctl00_Content_MarketInfoSplits1_Year")).select_by_visible_text(year)
        driver.find_element_by_css_selector("option[value=\""+year+"\"]").click()
        driver.find_element_by_css_selector("option[value=\""+year+"\"]").click()
        try:
            driver.find_element_by_link_text("1").click()
        except:
            print "already on page 1"


    def GetAllPages(self):

        self.driver.get(self.weblink)

        for year in xrange(2000,2015):
            print "YEAR="+str(year)
            self.selectyear(str(year),self.driver)
            html = self.driver.page_source
            maxpage=0
            print "Page=====================================1"
            maxpage=int(self.GetSplits(html))
            print "maxpage=",maxpage

            for i in xrange(2,maxpage+1):
                print "Page=====================================" +str(i)
                self.driver.find_element_by_link_text(str(i)).click()
                html = self.driver.page_source
                self.GetSplits(html)



