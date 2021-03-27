import requests
from bs4 import BeautifulSoup
import os
import traceback

def download(url, filename):
    if os.path.exists(filename):
        print('file exists!')
        return
    try:
        r = requests.get(url, stream=True, timeout=60)
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        return filename
    except KeyboardInterrupt:
        if os.path.exists(filename):
            os.remove(filename)
        raise KeyboardInterrupt
    except Exception:
        traceback.print_exc()
        if os.path.exists(filename):
            os.remove(filename)


if os.path.exists('konachan') is False:
    os.makedirs('konachan')

start = 6000
end = 7000
for i in range(start, end + 1):
    url = 'https://konachan.net/post?page=%d&tags=' % i
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    for img in soup.find_all('img', class_="preview"):
        #target_url = 'http:' + img['src']
        target_url = img['src']
        filename = os.path.join('konachan', target_url.split('/')[-1])
        download(target_url, filename)
    print('%d / %d' % (i, end))
