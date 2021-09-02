import requests 
from bs4 import BeautifulSoup
import re 
import time
import pandas as pd

# x = requests.get('https://tfc-taiwan.org.tw/articles/report')
# resp = BeautifulSoup(x.text,'lxml')
# lastPage = re.findall('[0-9]+',resp.select('#block-system-main .last a')[0]['href'])[0]
# print(f"共有 {lastPage} 頁")

def FactCheck(pages:int) -> pd.DataFrame():
    '''
        輸入欲爬取的頁數 (1頁10筆)
    '''

    MainCategory,SubCategory,Titles,Dates=[],[],[],[]
    for page in range(pages-1):
        url = f'https://tfc-taiwan.org.tw/articles/report?page={page}'
        r = requests.get(url)
        count = 1
        while ( (r.status_code != 200) & (count != 6) ):
            print(f'[斷線] 爬取第{page+1}時斷線，第{count}次重連...')
            time.sleep(2)
            r = requests.get(url)
            count += 1
        resp = BeautifulSoup(r.content.decode('utf-8'),'lxml')
        mainCategory = [ i.text.strip() for i in resp.select('.lineage-item-level-0 a')]
        subCategory = [ i.text.strip() for i in resp.select('.attr-tag a')]
        titles = [ i.text.strip() for i in resp.select('.entity-list-title a')]
        dates = [ re.findall('[0-9-]+',i.text.strip())[0] for i in resp.select('.post-date')]
        MainCategory.extend(mainCategory)
        SubCategory.extend(subCategory)
        Titles.extend(titles)
        Dates.extend(dates)
    
    df = pd.DataFrame({'更正層級':MainCategory,'文章分類':SubCategory,'文章標題':Titles,'發布日期':Dates})
    return df 

df = FactCheck(10)
df.to_csv('前十筆資料.csv',encoding='utf-8-sig',index=False)