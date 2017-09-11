from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from urllib.error import HTTPError
from urllib.error import URLError
import time
num = 0
#获取本页图片组的跳转链接
def getallhtml(url):
    htmls = gethtml(url)
    bsobj = BeautifulSoup(htmls,"html.parser")
    imgsites = bsobj.find("dl", {"class": "list-left"}).findAll("img")
    picsites= []
    for i in imgsites:
        picsites.append(i.attrs["src"])
    return picsites
#获取余下所有页面链接
def getnextshtml(url):
    nexts = []
    for i in range(2, 103):
        the = "http://www.mm131.com/xinggan/list_6_"+str(i)+".html"
        nexts.append(the)
    return nexts
#获取图片链接
def getthispics(url):
    htmls = gethtml(url)
    bsobj = BeautifulSoup(htmls, "html.parser")
    src = bsobj.find("div",{"class": "content-pic"}).find("img").attrs["src"]
    return src
#获取余下所有src
def getsrcs(src):
    srcs = []
    strs = src[:-5]
    for i in range(70):
        asrc = strs+str(i)+".jpg"
        srcs.append(asrc)
    return srcs

#多次获取链接尝试
def gethtml(url):
    maxNum = 40
    for tries in range(maxNum):
        try:
            html = urlopen(url)
            return html
        except:
            if tries< (maxNum-1):
                tries+=1
                print("拒绝{}次in{}".format(tries, maxNum))
                continue
            else:
                print("拒绝链接")
                break

#多次尝试下载
def downpic(src):
    maxNum = 40
    global num
    for tries in range(maxNum):
        try:
            urlretrieve(src,'%s.jpg'%num)
            num += 1
            time.sleep(1)
            print(num, end=' ')
            print('src='+src)
            break
        except URLError:
            if tries<(maxNum-1):
                print("拒绝{0}次in{1}".format(tries, maxNum))
                tries+=1
                continue
            else:
                print("拒绝链接")
                break
        except HTTPError:
            print("无此链接")
            break
        except:
            print("其他错误")
            pass

theurl = "http://www.mm131.com/xinggan/"
oldsrcs = getallhtml(theurl)
for i in oldsrcs:
    #downpic(i)
    num+=1
    evesrcs = getsrcs(i)
    for j in evesrcs:
        #downpic(j)
        num+=1
allhtml = getnextshtml(theurl)
for i in allhtml:
    newsrcs = getallhtml(i)
    for j in newsrcs:
        downpic(j)
        newevesrc = getsrcs(j)
        for k in newevesrc:
            downpic(k)

