from nsesql import NSESQL
from nsesql import SQLLITE3SQL_stock
import datetime
import time
import csv
import thread
from nsedownload import NseDownload
import threading
import sys
import os
from subprocess import check_output
from splitgrab import GrabSplitSelenium
from BeautifulSoup import BeautifulSoup
from splitadjust import SplitStock


def GetSplits(html):

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
            print csvout
        return maxpage

#OPEN,HIGH,LOW,CLOSE,VOLUME


def DBBulkUpdate(fname):
    i=NSESQL()
    i.CSVToDB(fname)

def NSEdtcheck(filedb,dt):
    nsedb = SQLLITE3SQL_stock(filedb)

    reccount = int(nsedb.Checkdt(dt))
    print reccount
    return reccount



def NSESQLmain():

    i=NSESQL()
#    i.CSVToDB("cm07JUL2004bhav.csv")

    #i=NseDownload()

#    yy=int(sys.argv[1])
    #yy=2003
    #print yy
 #   last_update=time.strptime(i.GetLastUpdate(yy),"%Y-%m-%d")
 #   dt=datetime.date(last_update.tm_year,last_update.tm_mon,last_update.tm_mday)




    dt =  datetime.date(2014,12,01)

    while dt <= datetime.date(2015,01,15):
        if NSEdtcheck("NSE.db",dt) > 0:
            print "record already exsist"
            dt=dt+ datetime.timedelta(days=1)
            continue;
        i.DownloadCSV(dt)
        fname="cm"+dt.strftime("%d%b%Y").upper()+"bhav.csv"
        if os.path.isfile(fname) == False:
            dt=dt+ datetime.timedelta(days=1)
            continue
        print "Processing "+fname
        print datetime.datetime.now().time()


        i.CSVToDB(fname)
        i.conn.close()
        check_output("c:\\sqllite\\sqlite3.exe NSE.db < mergedb.txt",shell=True)
        try:
            os.rename("stocks.db",(fname+".db"))
        except:
            print("file Already exsist")

        dt=dt+ datetime.timedelta(days=1)
        i.dbreopen()
        #time.sleep(1)


def splitmain():
    i=GrabSplitSelenium()
    #i.GetAllPages()
    #with open ("MarketInfoSplits.htm", "r") as myfile:
    #    data=myfile.read().replace('\n', '')
    #GetSplits(data)
    i=SplitStock()
    i.splitstock("PNB",10,2,"18/12/2014")


if __name__ == "__main__":
    NSESQLmain()

    #splitmain()


