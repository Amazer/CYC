#codeing=utf-8
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
import urllib
import urllib2
import cookielib


def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html


def getHtmlWithResponse(url):
    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read()
    except urllib2.URLError,e:
        if hasattr(e,'code'):
            print e.code
        if hasattr(e,'reason'):
            print e.reason

def getHtmlPost(url, valuesDic, Referer):
    data = urllib.urlencode(valuesDic)

    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64)'
    headers = {'User-Agent': user_agent}

    if Referer:
        headers['Referer'] = Referer

    request = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(request)
    return response.read()


def getHtmlGet(url, valuesDic):
    data = urllib.urlencode(valuesDic)
    getUrl = url + "?" + data
    request = urllib2.Request(getUrl)
    response = urllib2.urlopen(request)
    return response.read()


def getHtmlGet(url, valuesDic):
    data = urllib.urlencode(valuesDic)
    getUrl = url + "?" + data
    request = urllib2.Request(getUrl)
    response = urllib2.urlopen(request)
    return response.read()


def setProxy(proxy):
    enable_proxy = True
    proxy_handler = urllib2.ProxyHandler({"http": proxy})
    null_proxy_handler = urllib2.ProxyHandler({})

    if enable_proxy:
        opener = urllib2.build_opener(proxy_handler)
    else:
        opener = urllib2.build_opener(null_proxy_handler)
    urllib2.install_opener(opener)

def saveCookie(url,fileName):
    cookie = cookielib.MozillaCookieJar(fileName)
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    response=opener.open(url)
    cookie.save(ignore_discard=True,ignore_expires=True)

def loadCookie(fileName):
    cookie=cookielib.MozillaCookieJar()
    cookie.load(fileName,ignore_discard=True,ignore_expires=True)
    return cookie

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        #         pass
        print('<%s>' % tag)

    def handle_endtag(self, tag):
        #         pass
        print('<%s>' % tag)

    def handle_data(self, data):
        print('data:')

    def handle_comment(self, data):
        #         pass
        print('<!-- -->')

    def handle_entityref(self, name):
        #         pass
        print('&%s;' % name)

    def handle_charref(self, name):
        #         pass
        print('&#%s;' % name)

'''
getHtmlWithResponse:
    >>> print getHtmlWithResponse('https://www.baidu.com')
'''

# print getHtmlGet('https://www.baidu.com')
'''
html = getHtml("https://www.baidu.com")
parser = MyHTMLParser()

parser.feed(html)
parser.close()
'''
# searchStr={'input':'weather'}
# html=getHtmlPost('https://www.baidu.com',searchStr,None)
# print html
# parser = MyHTMLParser()
# parser.feed(html)
# parser.close()

page=1
url='http://www.qiushibaike.com/text/page/'+str(page)+'/'
html=getHtmlWithResponse(url)
print html

