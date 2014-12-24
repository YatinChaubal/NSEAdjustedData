from nsedownload import NseBhavcopy
import datetime
import csv
import thread

#OPEN,HIGH,LOW,CLOSE,VOLUME


if __name__ == "__main__":
    i=NseBhavcopy()
    for j in range(1,30):
        dt=datetime.date(2014,12,j)
        print "downloading S"+str(dt)
        i.GetBhavcopy(datetime.date(2014,11,j))
        '''
        try:
            fname = open("bhavcopcm"+dt.strftime("%d%b%Y")+"bhav.csv")
        except:
            continue

        today_stocks_csv = csv.reader(fname)
        for each_stock in today_stocks_csv:

            if each_stock[0] == "":
                continue
            print each_stock[0]

            stock_csv_file = open(str(each_stock[0]+".csv"),"a+")
            stock_csv_file.write(each_stock[1]+","+each_stock[2]+","+each_stock[3]+","+each_stock[4]+
                                ","+each_stock[5]+","+each_stock[6]+"\n")
'''



