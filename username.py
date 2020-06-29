import urllib.request
from bs4 import BeautifulSoup
links=[]
url = input('song: ')
if url.startswith('https') is False:
    query = urllib.parse.quote(url)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.find(attrs={'class':'yt-uix-tile-link'})['href'])

    try:
        vid = soup.find(attrs={'class': 'yt-uix-tile-link'})['href']
        url ='https://www.youtube.com' + soup.find(attrs={'class': 'yt-uix-tile-link'})['href']
        print(url)
    except:
        print('skipped ' + url)