import urllib2
import datetime
import zipfile
import os
import csv
import thread
import sqlite3
import time

#from win32com.client import Dispatch

class sql_stock():
	def __init__(self,db_file="stock.db"):
		self.db_file = db_file
		self.conn = sqlite3.connect(db_file,check_same_thread=False)
		self.cusror = self.conn.cursor()
		self.thread_cnt=0
		try:
			self.conn.execute('''CREATE TABLE stocks
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
					TOTTRDVAL integer,
					TIMESTAMP date,
					TOTALTRADES integer,
					ISIN text
                )''')
		except:
			print "Table already exsist continuing"

	def insert_rec(self,symbol,sr,o,h,l,c,ac,lst,pc,vol,TOTTRDVAL, timestamp, totaltrades,isin):

		sqlc = self.conn.execute("select * from stocks where timestamp='"+str(timestamp)+"' and SYMBOL='"+str(symbol)+"'")
		sql_cnt=len(sqlc.fetchall())
		if sql_cnt > 0:
			print "Record already present"+str(symbol)+str(timestamp)
		else:
			self.conn.execute('''INSERT INTO stocks VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
			                  (symbol,sr,o,h,l,c,ac,lst,pc,vol,TOTTRDVAL, timestamp, totaltrades,isin))
			#self.conn.commit()


	def insert_rec_threaded(self,symbol,sr,o,h,l,c,ac,lst,pc,vol,TOTTRDVAL, timestamp, totaltrades,isin):
		self.thread_cnt = self.thread_cnt + 1
		conn = sqlite3.connect(self.db_file,check_same_thread=False)
		sqlc = conn.execute("select * from stocks where timestamp='"+str(timestamp)+"' and SYMBOL='"+str(symbol)+"'")
		sql_cnt=len(sqlc.fetchall())
		if sql_cnt > 0:
			print "Record already present"+str(symbol)+str(timestamp)
		else:
			conn.execute('''INSERT INTO stocks VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
			                  (symbol,sr,o,h,l,c,ac,lst,pc,vol,TOTTRDVAL, timestamp, totaltrades,isin))

		self.thread_cnt = self.thread_cnt - 1
	def commit(self):
		self.conn.commit()




class NseBhavcopy:
	def __init__(self):

		self.hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
			'Accept-Encoding': 'none',
			'Accept-Language': 'en-US,en;q=0.8',
			'Connection': 'keep-alive'}
		self.sql_stock=sql_stock("stock.db")

	def converttoBhav(self,name,curdt):
		ifile  = open(name, "rb")
		reader = csv.reader(ifile)

#		f=open("bhavcop"+name,"w")
		next(reader, None)

		for row in reader:
			self.sql_stock.insert_rec(
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
			            curdt,
			            row[11],
			            row[12]
			            )
		self.sql_stock.commit()

#			f.write(row[0] + "," +
#			curdt.strftime("%Y%m%d") +
#			"," + row[2] + "," + row[3] +
#			"," + row[4] + "," + row[5] +
#			"," + row[8] + "\n")
#		ifile.close()

	def GetBhavcopy(self,Date=datetime.date.today()):
		curdt=Date
		yy=curdt.year
		mm=curdt.strftime("%b")
		dd=curdt.day

		if dd < 10:
			dd ="0"+str(dd)
		url="http://www.nseindia.com/content/historical/EQUITIES/"+str(yy)+"/"+str(mm).upper()+"/cm"+str(dd)+str(mm).upper()+str(yy)+"bhav.csv.zip"

		req = urllib2.Request(url, headers=self.hdr)

		fileavailable=1
		try:
			page = urllib2.urlopen(req)
		except urllib2.HTTPError, e:
			#print e.fp.read()
			fileavailable=0
			self.filename=""
			self.ValidData=0


		if fileavailable == 1:
			meta = page.info()
			file_size = int(meta.getheaders("Content-Length")[0])
			file_name = url.split('/')[-1]
			f = open(file_name, 'wb')
			file_size_dl = 0
			block_sz = 8192
			while True:
				buffer = page.read(block_sz)
				if not buffer:
					break

				file_size_dl += len(buffer)
				f.write(buffer)
				status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
				status = status + chr(8)*(len(status)+1)
			f.close()

			zfile=open(file_name, 'rb')
			z=zipfile.ZipFile(zfile)
			for name in z.namelist():
				outfile = open(name, 'wb')
				outfile.write(z.read(name))
				outfile.close()
				self.converttoBhav(name,curdt)
			zfile.close()
			self.filename=name
			self.ValidData=1
			os.remove(name)
			os.remove(file_name)







