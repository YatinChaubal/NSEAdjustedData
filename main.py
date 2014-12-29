from NSESQL import NSESQL
import datetime
import time
import csv
import thread
from nsedownload import NseDownload
import threading
import sys

#OPEN,HIGH,LOW,CLOSE,VOLUME


def DBBulkUpdate(fname):
    i=NSESQL()
    i.CSVToDB(fname)




if __name__ == "__main__":
    i=NSESQL()
#    i.CSVToDB("cm07JUL2004bhav.csv")

    #i=NseDownload()

    yy=int(sys.argv[1])
    #yy=2003
    print yy
    last_update=time.strptime(i.GetLastUpdate(yy),"%Y-%m-%d")
    dt=datetime.date(last_update.tm_year,last_update.tm_mon,last_update.tm_mday)
    print "Starting at "+str(dt)

    thread_cnt=0
    while dt <= datetime.date(yy,12,31):

        fname="cm"+dt.strftime("%d%b%Y").upper()+"bhav.csv"

        print "Processing "+fname
        print datetime.datetime.now().time()

        i.CSVToDB(fname)
        dt=dt+ datetime.timedelta(days=1)

