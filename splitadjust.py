import sqlite3
import csv
import datetime
import time



class SplitStock:
    def __init__(self,dbname="NSE.db"):
        self.dbname = dbname
        self.conn = sqlite3.connect(self.dbname)
        self.cursor = self.conn.cursor()

    def splitstock(self,symbol,ofv,nfv,date):
        #splitsql="update stocks set AdjClose = (AdjClose*?)/? where symbol =? and timestamp < ?",(ofv,nfv,symbol,date)
        dt=time.strptime(date,"%d/%m/%Y")
        sdate=str(dt.tm_year)+"-"+str(dt.tm_mon)+"-"+str(dt.tm_mday)+" 00:00:00"
        print sdate
        splitsql = "update stocks set AdjClose = ((AdjClose*"+str(nfv)+")/"+str(ofv)+") where symbol ='"+symbol+"' and timestamp < datetime(\""+sdate+"\")"
        self.cursor.execute(splitsql)
        self.conn.commit()


    def __del__(self):
        self.conn.close()

