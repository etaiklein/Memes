from  BeautifulSoup import *
from urllib2 import urlopen

import urllib2
from BeautifulSoup import BeautifulSoup
import ast

#works for titles that only have two categories
#gets the full title of a meme from it's ID#
def getFullTitleFromPage(url):
    with open("MemeFull.txt", "a") as f:
        try:
            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page)
            soup = str(soup).split("\n")[0]
            soup = soup.split("txt\":\"")
            top = soup[1].split("\"")[0]
            bottom = soup[2].split("\"")[0]
            
            mystring = top + " *^* " + bottom
            f.write(mystring + "\n")
        except:
            pass
    
#works for titles that have multiple categories    
#gets the full title of a meme from it's ID#
def getFullTitleFromPage2(url, title):
    with open("MemeFull.txt", "a") as f:
        try:
            page = urllib2.urlopen(url)
            html = page.read()
            adict = ast.literal_eval(html)
            caplist = adict.get('caps', [])
            mystring = ""
            
            for cap in caplist:
                if mystring == "":
                    mystring += cap.get('txt', '').strip('"')
                else:
                    mystring += " *^* " + cap.get('txt', '').strip('"')
            
            
            f.write(title + " - " + mystring + "\n")
        except:
            pass
        

#scrapes all titles from a set of addresses
def getAllTitles():
    with open("MemeIDs.txt", "r") as f: 
        idlist = f.readlines()
        for ID in idlist:
            myID = ID.split(" - ")[1]
            title = ID.split(" - ")[0]
            getFullTitleFromPage2("http://www.quickmeme.com/make/get_data/?id=" + myID, title)
        

#Gets the max page number for a list of things across mulitple pages
def getMaxPage(url):
    try:
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        pages = soup.find(id="pagination")
        mymax = pages.find("a", { "class" : "next"}).previousSibling.previousSibling.string
        return int(mymax)
    except:
        pass
    return 0
        



#Meme Types
#Gets the addresses for different types of memes for each page
def getAllTypeAddresses(url):
    max = getMaxPage(url)
    if max != 0:
        for i in xrange(max):
            myurl = url + "/submissions/" +  str(i+1) + "/"
            getMemeTypeAddresses(myurl)
    else:
        getMemeTypeAddresses(url)

#Meme Types on a page
#Takes a page of different types of memes and gets the address for each meme on a page
def getMemeTypeAddresses(url3):
    with open("MemeTypesUp.txt", "a") as f: 
    #memes = [] #holds relative addresses like "/Philosoraptor"
        try:
            page = urllib2.urlopen(url3)
            soup = BeautifulSoup(page)
        ##For each page of popular memes, get meme:
            for thumbTag in soup.findAll("div" , { "class" : "memeThumb"}): #cf above
                link = thumbTag.find("a")
                f.write(link.attrs[0][1] + "\n")
        except:
            pass



#Gets all meme addresses for all meme types
def getIDsAllTypes():
    #opens the types to get the addresses of individual memes
    with open("MemeTypesUp.txt", "r") as f: 
        memes = f.readlines()
        for title in memes:
            myurl = "http://www.quickmeme.com" + title.strip("\n")
            getAllIDs(myurl, title)

#Meme IDs
#Takes a page of different types of memes gets the IDs for all the memes on each page
def getAllIDs(url, title):
    myMax = getMaxPage(url)
    if myMax != 0:
        for i in xrange(myMax):
            myurl = (url + "popular/" +  str(i+1) + "/")
            getMemeIDs(myurl, title)
    else:
        getMemeIDs(url, title)
        

#gets IDs for all IDs on a single page
def getMemeIDs(url, title):
    with open("MemeIDs.txt", "a") as f: 
        try:
            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page)
            thumbTag = soup.find("div" , { "class" : "memeThumb"}) 
            for ID in thumbTag.findAll("a"):
                f.write(title.strip("\n") + " - " + str(ID).split("#id=")[1].split("&")[0] + "\n")        
        except:
            pass    
            

#Gets all titles for all meme pages of all types
def getAllTitlesForAllIDs(url):
    getAllTypeAddresses(url)
    getIDsAllTypes()
    getAllTitles()
    
