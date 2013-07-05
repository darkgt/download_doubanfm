# coding: utf-8
 
from BeautifulSoup import BeautifulSoup
import urllib, urllib2, cookielib, re, json, eyeD3, os, copy

import download

base_url = 'http://music.douban.com%s'

def get_ssids(album):
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    urllib2.install_opener(opener)
    req = urllib2.Request(base_url % album)
    req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')
    content = urllib2.urlopen(req, timeout=20).read()
    soup = BeautifulSoup(str(content))
    ret = {}
    for li in soup.findAll('li', {'class' : 'song-item'}):
        ret[li['id']] = li['data-ssid']
    album_name = copy.copy(soup.find('h1').find('span').contents[0].decode('gb2312'))
    picurl = copy.copy(soup.find('a', {'class' : 'nbg'})['href'].decode('gb2312'))
    return ret, album_name, picurl

def main(album):
    #album = raw_input('album:')
    ssids, album_name, picurl = get_ssids(album)
    print 'all', len(ssids), 'songs'
    for sid, ssid in ssids.iteritems():
        ret = download.handle(sid, ssid, album_name, picurl)
        print ret
 
if __name__ == '__main__':
    #main()
    doc = 'album.txt'
    con = open(doc, 'r').readlines()
    for url in con:
        main(url[23:])
