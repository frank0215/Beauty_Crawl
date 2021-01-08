import requests
from bs4 import BeautifulSoup
import re
from urllib.request import urlretrieve
import os


def main():
    count = 0
    articlelist = askArticle(1)
    count += saveImg(articlelist)
    print(f'{count} images have been downloaded')

def askArticle(page=1):
    
    url = 'https://www.jkforum.net/forum-535-{}.html'.format(page)

    response = requests.get(url)
    #print(response.text)
    soup = BeautifulSoup(response.text, 'lxml')
    #print(soup)
    articles = soup.select('form li')

    articlelist = []
    for article in articles:
        for datalist in article('em'):
            for data in datalist('span'):
                articleInfo = []
                articleInfo.append(data.get('title'))
                
        for datalist in article('h3'):
            articleUrl = 'https://www.jkforum.net/' + datalist.select_one('a').get('href')
            articleInfo.append(articleUrl)
            articleTitle = datalist.select_one('a').get('title')
            articleInfo.append(articleTitle)
            
        articlelist.append(articleInfo)
        
    return articlelist



def saveImg(articlelist):
    filedir = 'D:\Beauty\JKF_AV'
    count = 0
    j=0
    z=0
    for i in range(len(articlelist)):
        date = articlelist[i][0]
        title = articlelist[i][2]
        r = re.compile('(　|！|「|」|，|…|、|\.)')
        title = r.sub('', title)
        newTitle = date + ' ' +title
        path = os.path.join(filedir, newTitle)
        if os.path.isdir(path):
            continue
        elif not os.path.isdir(path):
            os.mkdir(path)

        response = requests.get(articlelist[i][1])
        soup = BeautifulSoup(response.text, 'lxml')
        imgUrl = soup.select('ignore_js_op img')
        for img in imgUrl:
            imgFile = img.get('zoomfile')
            print(imgFile)
            try:
                imgName = imgFile.split('/')[-1][-10:]
            except Exception as e:
                print(e)
            write_in = os.path.join(filedir, newTitle, imgName)
            urlretrieve(imgFile, write_in)
            count += 1
        
        j+=1
        if j==1:
            break

    return count

if __name__ == "__main__":
    main()
    