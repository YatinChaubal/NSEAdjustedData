from GrabSplit import GrabSplitSelenium
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

if __name__ == "__main__":

    #i=GrabSplitSelenium()
    #i.GetAllPages()
    #with open ("MarketInfoSplits.htm", "r") as myfile:
    #    data=myfile.read().replace('\n', '')
    #GetSplits(data)
    i=SplitStock()
    i.splitstock("PNB",10,2,"18/12/2014")



