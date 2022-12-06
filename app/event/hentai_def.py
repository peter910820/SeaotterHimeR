import requests
from bs4 import BeautifulSoup

def nhentai_Search(six_numbers):
    six_numbers = six_numbers[1:]
    return "https://nhentai.net/g/" + six_numbers

def wancg_Search(five_numbers):
    five_numbers = five_numbers[1:]
    r = requests.get(f'https://www.wnacg.org/photos-index-aid-{five_numbers}.html')
    soup = BeautifulSoup(r.text,'lxml')
    data = soup.select("h2")
    try:
        return data[0].text + '\nhttps://www.wnacg.org/photos-index-aid-{five_numbers}.html'
    except:
        return '沒有這個本子!'