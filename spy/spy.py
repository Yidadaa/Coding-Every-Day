import urllib.request as urllib2
import re
import sys

def downloadMusic(url, name):
    try:
        html = urllib2.urlopen(url)
    except ValueError as e:
        print('invalid url')
        return False
    content = str(html.read().decode('utf-8', 'ignore'))
    playurlBeginIndex = content.find('"playurl"')
    playurlEndIndex = content.rfind(',"playurl_video"')
    if playurlBeginIndex * playurlEndIndex <= 0:
        return False
    musicName = content[content.find('"song_name"'):content.rfind(',"tail_name"')].replace('"', '').replace('song_name:', '')
    playurlRaw = content[playurlBeginIndex : playurlEndIndex]
    playurl = playurlRaw.replace('"', '').replace('playurl:', '')
    music = urllib2.urlopen(playurl)
    with open(sys.path[0] + '/' + musicName + '-' + name + '.m4a', 'wb') as f:
        f.write(music.read())
    return True

def readInfo(filepath):
    with open(sys.path[0] + '/' + filepath) as f:
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

readInfo("test.csv")