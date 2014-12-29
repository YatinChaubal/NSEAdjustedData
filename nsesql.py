__author__ = 'Yatin'
from nsedownload import NseDownload
import sqlite3
import csv
import datetime
import MySQLdb


class SQL_stock():
    def __init__(self):

        try:
            self.conn = MySQLdb.connect(host="localhost",user="StockDBAdmin",passwd="StockDBAdmin$123",db="NSE")
            self.cursor = self.conn.cursor()
        except:
            self.conn = MySQLdb.connect(host="localhost",user="StockDBAdmin",passwd="StockDBAdmin$123")
            self.cursor = self.conn.cursor()
            self.cursor.execute('CREATE DATABASE NSE')
            self.cursor = self.conn.cursor()
            self.conn.close()
            self.conn = MySQLdb.connect(host="localhost",user="StockDBAdmin",passwd="StockDBAdmin$123",db="NSE")
            self.cursor = self.conn.cursor()



        try:
            self.cursor.execute('''CREATE TABLE stocks
                 (SYMBOL Text,
                    series Text,
                    OPEN real,
                    HIGH real,
                    LOW real,
                    CLOSE real,
                    AdjCLOSE real,
                    LAST real,
                    PREVCLOSE real,
                    Volume integer,
                    TOTTRDVAL real,
                    TIMESTAMP date,
                    TOTALTRADES integer,
                    ISIN text
                )''')
        except:
            print "Table already exsist continuing"

    def __del__(self):
        self.conn.close()


    def insert_rec(self,symbol,sr,o,h,l,c,ac,lst,pc,vol,TOTTRDVAL, timestamp, totaltrades,isin):

        self.cursor.execute("select count(*) from stocks where timestamp='"+str(timestamp)+
                                 "' and SYMBOL='"+str(symbol)+"' and series ='"+str(sr)+"'")

        if self.cursor.fetchone()[0] == 0:

            ins_query_sql = ("INSERT INTO stocks VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            ins_query_val = (symbol,sr,o,h,l,c,ac,lst,pc,vol,TOTTRDVAL, timestamp, totaltrades,isin)

            self.cursor.execute(ins_query_sql,ins_query_val)

    def GetLastUpdate(self,year):
        self.cursor.execute("select max(timestamp) from stocks where date(timestamp) < '"+str(year)+"-12-31 00:00:00'")
        return str(self.cursor.fetchone()[0])




    def commit(self):
        self.conn.commit()


class NSESQL(NseDownload,SQL_stock):
    def __init__(self,DownloadDir="",Deletezip='y',DeleteCSV='n'):
        SQL_stock.__init__(self)
        NseDownload.__init__(self,DownloadDir=DownloadDir,Deletezip=Deletezip)
        print self.DownloadDir

    def CSVToDB(self,name=""):

        try:
            ifile  = open(name, "rb")
        except:
            return 0
        reader = csv.reader(ifile)
        next(reader, None)
        reccnt=1
        for row in reader:

            reccnt=reccnt+1
            try:
                if row[0] == "SYMBOL":
                    continue
            except:
                continue

            try:
                isin=row[12]
            except:
                isin=0
            try:
                totaltran=row[11]
            except:
                totaltran="0"
            if totaltran == "":
                totaltran=0

            if isin == "EQ":
                totaltran=0
                self.insert_rec(
                        row[11],
                        row[12],
                        row[13],
                        row[14],
                        row[15],
                        row[16],
                        row[16],
                        row[17],
                        row[18],
                        row[19],
                        row[20],
                        datetime.datetime.strptime(row[21],"%d-%b-%Y"),
                        0,
                        isin
                        )

            self.insert_rec(
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                        row[4],
                        row[5],
                        row[5],
                        row[6],
                        row[7],
                        row[8],
                        row[9],
                        datetime.datetime.strptime(row[10],"%d-%b-%Y"),
                        totaltran,
                        isin
                        )
        self.commit()
    def DownloadToDB(self,Date):
        csvfileloc = str(self.DownloadCSV(Date=Date))
        if len(csvfileloc) != 0 :
            self.CSVToDB(csvfileloc)





