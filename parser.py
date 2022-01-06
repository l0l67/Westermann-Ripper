import json
import urllib.request
import re

fileData = ""
urls = []

def parserJson():
    global urls, fileData
    jsonData = json.load(open('files.har', 'r'))
    
    counter = 3
    while True:
        try:
            url = jsonData['log']['entries'][counter]['request']['url']
        except IndexError:
            break
        if url.endswith('.png'):
            urls.append(url)
        counter += 1

def downloadImages():
    global urls
    for url in urls:
        file_name = re.sub('[^0-9]','', url[-7:]) + '.png'

        urllib.request.urlretrieve(url, file_name)
        print('Finished: ' + file_name)    

if __name__ == "__main__":
    parserJson()
    downloadImages()
