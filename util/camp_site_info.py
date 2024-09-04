import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from sys import argv
import os


def create_date_str_path():
    return time.strftime("%m_%d_%Y/")


def scrape_lat_long(html):
    soup=BeautifulSoup(html, 'html.parser')
    divs=soup.find_all('div', attrs={'class': 'right-box'})
    latitude=None
    longitude=None
    for div in divs:
        if 'Latitude' in div.text:
            latitude=div.find_next_sibling('div').text.strip()
        if 'Longitude' in div.text:
            longitude=div.find_next_sibling('div').text.strip()
        if latitude and longitude:
            break
    return (latitude, longitude)


def fetch_camp_site_content(url):
#    headers={'User-Agent': 'Pilgrim/0.0.1'}
#    headers={'User-Agent': 'Pilgrim/0.0.2'}
    headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0'}
    response=requests.get(url, headers=headers, timeout=10)
    return response.content


if __name__=='__main__':
    CAMP_SITE_URLS_PATH=f"data/camp_site_urls/{create_date_str_path()}"
    CAMP_SITE_URLS_FILENAME='camp_site_urls.csv'
    CAMP_SITE_INFO_PATH=f"data/camp_site_info/{create_date_str_path()}"
    CAMP_SITE_INFO_FILENAME='camp_site_info.csv'
    SLEEP_TIME=2

    try:
        batch_start=int(argv[1])
        batch_end=int(argv[2])
    except IndexError:
        raise SystemExit(f'Usage: {argv[0]} <batch_start> <batch_end>')

    df=pd.read_csv(CAMP_SITE_URLS_PATH+CAMP_SITE_URLS_FILENAME)
    if batch_end > df.shape[0] + 1:
        raise SystemExit(f"batch end: {batch_end} is greater than maximum batch end: {df.shape[0]}.")
    df=df.loc[batch_start:batch_end-1]
    for i in range(batch_start, batch_end):
        url=df.loc[i, 'URL']
        print(f'Number in Batch {i+1}')
        print(f'Fetching camp site content from {url}')
        html=fetch_camp_site_content(url)
        latitude, longitude=scrape_lat_long(html)
        df.loc[i, 'LATITUDE']=latitude
        df.loc[i, 'LONGITUDE']=longitude
        time.sleep(SLEEP_TIME)

    write_header=False if os.path.exists(CAMP_SITE_INFO_PATH) else True

    if write_header:
        os.mkdir(CAMP_SITE_INFO_PATH)

    df.to_csv(CAMP_SITE_INFO_PATH+CAMP_SITE_INFO_FILENAME,
              mode='a',
              index=False,
              header=write_header)


# TODO TEST BATCH END LOGIC TO ENSURE WE CAN GET INFO FOR ALL CAMP SITES, BUT THROW ERROR WHEN BATCH END IS TOO BIG
