import requests
from bs4 import BeautifulSoup
import datetime
import re
from urllib.request import urlretrieve
import os

def askArticle(start_date, period=0, start_page=0, end_page=1):
    #url = 'http://luxutvpremium.blog.fc2.com'
    now_date = datetime.datetime.now()
    end_current_page = end_page
    start_current_page = start_page
    current_period = period
    start_date = datetime.datetime.strptime(start_date, '%Y/%m/%d')
    end_date = start_date - datetime.timedelta(days=(period+1))
    articlelist = []
    for i in range(start_current_page, end_current_page):
        url = 'http://luxutvpremium.blog.fc2.com/page-{}.html'.format(i)
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'lxml')
        articles = soup.select('h2.topentry_title a')
        dates = soup.select('span.date')

        storage = [article.get('href') for article in articles]

        datelist = [datetime.datetime.strptime(date.text.strip('\n'), '%Y/%m/%d') for date in dates]

        #articlelist = list(map(list,[article for article in zip(datelist, articlelist) if (article[0] <= start_date) and (start_date - article[0] < datetime.timedelta(days=(period+1)))]))
        for article in zip(datelist, storage):
            if (article[0] <= start_date) and (start_date - article[0] < datetime.timedelta(days=(period+1))):
                articlelist.append(list(article))

        next_url = soup.select('a.pager_next')[0].get('href')
        
    
    #checkLeft(url,start_date)

    if start_date < now_date and len(articlelist)==0 and not(start_date > datelist[-1] and not(start_date in datelist)):
        start_current_page += 1
        end_current_page += 1
        return askArticle(datetime.datetime.strftime(start_date, '%Y/%m/%d'), current_period, start_current_page, end_current_page)
    elif checkLeft(next_url, end_date):
        end_current_page += 1
        return askArticle(datetime.datetime.strftime(start_date, '%Y/%m/%d'), current_period, start_current_page, end_current_page)
    else:
        return articlelist

def checkLeft(next_url, end_date):
    res = requests.get(next_url)
    soup = BeautifulSoup(res.text, 'lxml')
    dates = soup.select('span.date')
    datelist = [datetime.datetime.strptime(date.text.strip('\n'), '%Y/%m/%d')for date in dates]
    if end_date <= datelist[0]:
        return True
    else:
        return False

def saveImg(articlelist):
    count = 0
    total_img = []
    datelist = []
    titlelist = []
    for article in articlelist:
        res = requests.get(article[1])
        soup = BeautifulSoup(res.text, 'lxml')
        imglist = soup.select('img')
        saveImg = [img .get('src') for img in imglist if 'https://image.mgstage.com/images/' in img.get('src')]
        count += len(saveImg)     
        total_img.append(saveImg)
        datelist.append(article[0])
        texts = soup.select('div.topentry_text')
        reg = re.compile(r'<br/>品番：(.*?)<br/>')
        match = reg.search(str(texts[0])).group(1)
        title = '品番：' + match
        titlelist.append(title)
        
    return total_img, datelist, titlelist, count

def downloadImg(total_img, datelist, titlelist):
    filedir = 'D:\\Beauty\\AV2'
    for element in zip(total_img, datelist, titlelist):
        newTitle = datetime.datetime.strftime(element[1], '%Y-%m-%d') + ' ' + element[2].replace('品番：','')
        #print(newTitle)
        path = os.path.join(filedir, newTitle)
        if os.path.isdir(path):
            continue
        elif not os.path.isdir(path):
            os.mkdir(path)
        for img in element[0]:
            print(img)
            fileName = img.split('/')[-1]
            #print(fileName)
            write_in = os.path.join(filedir, newTitle, fileName)
            urlretrieve(img, write_in)

def main():
    yester_date = datetime.datetime.now() - datetime.timedelta(days=1)
    yester_date = datetime.datetime.strftime(yester_date, '%Y/%m/%d')
    articlelist = askArticle(yester_date)
    #articlelist = askArticle('2020/5/3')
    imglist, datelist, titlelist, count = saveImg(articlelist)
    #downloadImg(imglist, datelist, titlelist)
    for i, imgs in enumerate(imglist):
        print(datetime.datetime.strftime(datelist[i], '%Y/%m/%d'), titlelist[i])
        for img in imgs:
            print(img)
        
    print(f'{count} images have been downloaded')
        
    

if __name__ == "__main__":
    main()