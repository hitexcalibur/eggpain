#coding=gbk
import urllib,urllib2,cookielib,re,datetime
import os

def getPageHtml(uri):
    req = urllib2.Request(uri)
    return urllib2.urlopen(req).read()
    
def getFileContent():
    fp = open("test.txt", 'r')
    content = fp.read()
    fp.close()
    return content
    
def getName(str):
    i = 0
    tmp = ''
    while (i < len(str)):
        if (str[i] != '<'):
            if (str[i] != '\n'):
                tmp = tmp + str[i]
        else:
            while(str[i] != '>'):
                i = i + 1
        i = i + 1
    return tmp

def login():
    pattern = re.compile("<input type=\"hidden\" name=\"formhash\" value=\"\w*\" \/>")
    content = getPageHtml('http://www.lightnovel.cn')
    formhash = pattern.findall(content)
    if (len(formhash) > 0):
        formhash = formhash[0]
        formhash = formhash[-12:-4]

        cookieJar = cookielib.CookieJar()
        cookie_support= urllib2.HTTPCookieProcessor(cookieJar)
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)      

        postdata=urllib.urlencode({
             'fastloginfield':'username',
             'username':'wxinuyasha',
             'password':'19891225',
             'formhash':formhash
        })
      
        req = urllib2.Request(
              url = 'http://www.lightnovel.cn',
              data = postdata,
        )
        result = urllib2.urlopen(req).read()
        print "Login Successfully!!!"

def getAttachment(dirName, url):
    pageContent = getPageHtml(url)
    pattern = re.compile('<a href=\"attachment\.php\?aid=.*>.*<\/a>')
    anchors = pattern.findall(pageContent)
    for anchor in anchors:
        attachUrl = "http://www.lightnovel.cn/" + anchor.split('"')[1]
        namePattern = re.compile('>[^<>].*[^<>]<\/')
        name = namePattern.findall(anchor)
        fileName = name[0][1:-2]
        print fileName
        fileName = dirName + '\\' + fileName
        download(attachUrl, fileName)
            
def download(url,fileName):
    urllib.urlretrieve(url, fileName)

def createFolder(path, folderName ):
    if os.path.isdir(path):
        newFolderName = path + '\\\\' + folderName
        if os.path.isdir( newFolderName ):
            print newFolderName," Exists already "
        else:
            os.mkdir( newFolderName )
            print newFolderName," Create OK "
        return newFolderName

rootPath = "."
login()
indexContent = getPageHtml('http://www.lightnovel.cn/viewthread.php?tid=78222&extra=page%3D1')
#indexContent = getFileContent()
keyWord = raw_input("Please input the name of the novel: ")
pString = '<a href=.*' + keyWord + '[\s\S]*?</a>'
pattern = re.compile(pString)
anchors = pattern.findall(indexContent)
if len(anchors) > 0:
    count = 1
    nowPath = createFolder(rootPath, keyWord)
    for anchor in anchors:
        name = getName(anchor)
        print name
        tempUrl = anchor.split('"')[1]
        newPath = createFolder(nowPath, str(count))
        getAttachment(newPath, tempUrl)
        count = count + 1


