import requests
from bs4 import BeautifulSoup
r = requests.get('https://www.wnacg.org/photos-index-aid-181728.html')

r2 = requests.get('https://www.wnacg.org/photos-index-aid-1817281.html')
a = BeautifulSoup(r.text,'lxml')
data = a.select("h2")
try:
    print(data[0].text)
except:
    print('沒有這個本子!')