'''This project work on download files from
    UCI Machine Learning Repository
    https://archive.ics.uci.edu/ml/index.php

    import the target url and download all the file in
    the download directory
'''

import requests
import bs4
from urllib.parse import urljoin
import os

def get_soup(httplink):
    '''download the webside and transfer to soup
    '''
    html = requests.get(httplink).text
    return bs4.BeautifulSoup(html, 'html.parser')

# input targetUrl
# targetUrl = 'https://archive.ics.uci.edu/ml/datasets/Census+Income'
targetUrl = input('the source url from UCI:')

# find the root source link and data describtion
soup = get_soup(targetUrl)
source_link = soup.find_all(valign='top')[1].a.get('href')
full_source_link = urljoin(targetUrl, source_link)
target_name = soup.find(class_='heading').text

# goto download page
soup = get_soup(full_source_link)
file_tree = soup.body.table.find_all('tr')

# download the files
# prepare the directory
userPath = '/Users/' + os.listdir('/Users/')[0]
localPath = userPath + '/Downloads/' + target_name
localPath = localPath+'_1' if os.path.exists(localPath) else localPath
os.mkdir(localPath)
print(localPath)

# download and save each file to local
for branch in file_tree[3:-1]:
    name = branch.a.get('href')
    path = urljoin(full_source_link, name)
    print('files name:-> ' + name)
    html = requests.get(path).text
    with open(localPath+'/'+name, 'w') as f:
        f.write(html)
