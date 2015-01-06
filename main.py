from NSESQL import NSESQL
import datetime
import time
import csv
import thread
from nsedownload import NseDownload
import threading
import sys
import os
from subprocess import check_output

#OPEN,HIGH,LOW,CLOSE,VOLUME


def DBBulkUpdate(fname):
    i=NSESQL()
    i.CSVToDB(fname)




if __name__ == "__main__":
    i=NSESQL()
#    i.CSVToDB("cm07JUL2004bhav.csv")

    #i=NseDownload()

#    yy=int(sys.argv[1])
    #yy=2003
    #print yy
 #   last_update=time.strptime(i.GetLastUpdate(yy),"%Y-%m-%d")
 #   dt=datetime.date(last_update.tm_year,last_update.tm_mon,last_update.tm_mday)




    dt =  datetime.date(2014,10,01)
    while dt <= datetime.date(2014,12,31):
        i.DownloadCSV(dt)
        fname="cm"+dt.strftime("%d%b%Y").upper()+"bhav.csv"
        if os.path.isfile(fname) == False:
            dt=dt+ datetime.timedelta(days=1)
            continue
        print "Processing "+fname
        print datetime.datetime.now().time()


        i.CSVToDB(fname)
        i.conn.close()
        check_output("sqlite3.exe NSE.db < mergedb.txt",shell=True)
        try:
            os.rename("stocks.db",(fname+".db"))
        except:
            print("file Already exsist")

        dt=dt+ datetime.timedelta(days=1)
        i.dbreopen()
        #time.sleep(1)

