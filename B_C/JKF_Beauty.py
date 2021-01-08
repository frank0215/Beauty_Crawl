import requests
from bs4 import BeautifulSoup
import os
from urllib.request import urlretrieve
import re



def main():
    articlelist = askArticle(2)
    count = 0
    count += saveImg(articlelist)
    print('{} articles have been downloaded!'.format(count))


def askArticle(page=1):
    url = 'https://www.jkforum.net/forum-736-{}.html'.format(page)
    response = requests.get(url)
    # print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)
    articles = soup.select('form li')

    articlelist = []
    for article in articles:
        for datalist in article('em'):
            #print(datalist)
            for data in datalist('span'):
                #print(data)
                articleInfo = []
                articleTime = data.get('title')
                articleInfo.append(articleTime)


        for datalist in article('h3'):

            articleUrl = 'https://www.jkforum.net/' + datalist.select_one('a').get('href')
            articleInfo.append(articleUrl)
            #print(articleUrl)
            articleTitle = datalist.select_one('a').text
            articleInfo.append(articleTitle)
            #print(articleTitle)

        articlelist.append(articleInfo)        
    
    # length = len(articlelist)
    # for i in range(length):
    #     print(articlelist[i][1])
    #print(articlelist)

    return articlelist


def saveImg(articlelist):
    filedir = 'D:\\Beauty\\JKF_Beauty'
    count = 0
    for i in range(len(articlelist)):
        # print(articlelist[i][1])
        # print(articlelist)
        date = articlelist[i][0]
        title = articlelist[i][2]
        r = re.compile('(　|！|「|」|，|…|、|\.)')
        title = r.sub('', title)
        newTitle = (date+title)
        #print(newTitle)
        path = os.path.join(filedir, newTitle)
        if os.path.isdir(path):
            continue
        elif not os.path.isdir(path):
            os.mkdir(path)

        response = requests.get(articlelist[i][1])
        soup = BeautifulSoup(response.text, 'html.parser')
        url = soup.select('ignore_js_op img')
        for imgUrl in url:
            imgFile = imgUrl.get('zoomfile')
            print(imgFile)
            try:
                fileName = imgFile.split('/')[-1][-10:]
            except Exception as e:
                print(e)
            write_in = os.path.join(filedir, newTitle, fileName)
            urlretrieve(imgFile, write_in)
        count += 1
        
    return count 

if __name__=="__main__":
    main()
    