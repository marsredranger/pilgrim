import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from sys import argv
import os

def scrape_lat_long(html):
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find_all('div', attrs={'class': 'right-box'})
    latitude = None
    longitude = None
    for div in divs:
        if 'Latitude' in div.text:
            latitude = div.find_next_sibling('div').text.strip()
        if 'Longitude' in div.text:
            longitude = div.find_next_sibling('div').text.strip()
        if latitude and longitude:
            break
    return (latitude, longitude)

def fetch_camp_site_content(url):
    headers = {'User-Agent': 'Camping Tripper/0.0.1'}
    response = requests.get(url, headers=headers)
    return response.content 

if __name__ == '__main__':
    try:
        batch_start = int(argv[1])
        batch_end = int(argv[2])
    except IndexError as e:
        raise SystemExit(f'Usage: {argv[0]} <batch_start> <batch_end>')

    CAMP_SITE_CSV_PATH = './camp_site_urls.csv'
    CAMP_SITE_INFO_CSV_PATH = './camp_site_info.csv'
    SLEEP_TIME = 5
    
    df = pd.read_csv(CAMP_SITE_CSV_PATH)
    df = df.loc[batch_start:batch_end-1]

    for i in range(batch_start, batch_end):
        url = df.loc[i, 'URL']
        print(f'Number in Batch {i+1}')
        print(f'Fetching camp site content from {url}')
        html = fetch_camp_site_content(url)
        latitude, longitude = scrape_lat_long(html)
        df.loc[i, 'LATITUDE'] = latitude
        df.loc[i, 'LONGITUDE'] = longitude
        time.sleep(SLEEP_TIME)

    write_header = False if os.path.exists(CAMP_SITE_INFO_CSV_PATH) else True
    df.to_csv(CAMP_SITE_INFO_CSV_PATH, mode='a', index=False, header=write_header)

