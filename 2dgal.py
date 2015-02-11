import urllib,urllib2,cookielib,re,datetime
import string

def getPageHtml(uri):
    req = urllib2.Request(uri)
    return urllib2.urlopen(req).read()
    #return urllib.urlopen(uri).read()

def login():
    if True:

        cookieJar = cookielib.CookieJar()
        cookie_support= urllib2.HTTPCookieProcessor(cookieJar)
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
      

        postdata=urllib.urlencode({
             
             'pwuser':'wxinuyasha',
             'pwpwd':'19891225',
             'hideid':'0',
             'cktime':'31536000',
             'step':'2'

        })
      
        headers = {
             'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
             'referer':'http://bbs.kafan.cn'
        }

      
        req = urllib2.Request(
              url = 'http://bbs.9gal.com/login.php',
              data = postdata,
              #headers = headers
        )
        result = urllib2.urlopen(req).read()
        print "Login Successfully!!!"

def getNewGame():
    count = 0
    pageContent = getPageHtml('http://bbs.9gal.com/kf_share.php?ti=41&new=1')
    date = getDateString('-')
    print date
    #date = '11-25'
    pString = '<tr onmouseover="this.style.backgroundColor=\'#ffffcc\'" onmouseout="this.style.backgroundColor=\'#ffffff\'"><td class="kf_share2">' + date + '[\s\S]*?</td></tr>'
    pattern = re.compile(pString)
    anchors = pattern.findall(pageContent)
    #print pString

    for anchor in anchors:
        #print anchor
        parts = anchor.split('</font>')[-1].split('</a>')
        print parts[0]
        count = count + 1
    print count
        


def getDateString(ch):
    from datetime import date
    format = "%m" + ch + "%d"
    todayStr = date.today().strftime(format)
    return todayStr
      
login()
getNewGame()