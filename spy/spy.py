#-*- coding: UTF-8 -*-
import urllib2
from urllib2 import URLError
import re

def downloadMusic(url, filename):
    try:
        html = urllib2.urlopen(url)
    except ValueError as e:
        print('invalid url')
        return False
    content = html.read()
    playurlBeginIndex = content.find('"playurl"')
    playurlEndIndex = content.rfind(',"playurl_video"')
    if playurlBeginIndex * playurlEndIndex <= 0:
        return False
    musicName = content[content.find('"song_name"'):content.rfind('"tail_name"')].replace('"', '')
    playurlRaw = content[playurlBeginIndex : playurlEndIndex]
    playurl = playurlRaw.replace('"', '').replace('playurl:', '')
    music = urllib2.urlopen(playurl)
    with open(str(len(filename)) + '.m4a', 'wb') as f:
        f.write(music.read())
    return True

def readInfo(filepath):
    with open(filepath) as f:
        rawContent = f.readlines();
    dataList = []
    for line in rawContent[1:]:
        info = line.strip().split(',')[6:]
        dataList.append({
            'name': info[0],
            'url': info[2]
        })
    for info in dataList:
        downloadMusic(info['url'], info['name'])

readInfo('test.csv')