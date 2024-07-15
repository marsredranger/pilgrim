from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import parse_qs
import requests
import time
import pandas as pd
import os


def create_date_str_path():
    return time.strftime("%m_%d_%Y/")


def scrape_ending_page():
    url = BASE_URL+str(STARTING_PAGE)
    attrs = {'aria-label': 'Last pate'}
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    ending_page_element = soup.find_all(attrs=attrs)
    ending_page_url = ending_page_element[0]['href']
    parsed_ending_page_url = urlparse(ending_page_url)
    ending_page = int(parse_qs(parsed_ending_page_url.query)['page'][0])
    return ending_page


def scrape_urls():
    camp_sites = []
    attrs = {'class': 'usa-link'}
    for page in range(STARTING_PAGE, ending_page+1):
        url = BASE_URL + str(page)
        print(f'Sending GET request to {url}')
        response = requests.get(url, headers=HEADERS)
        print(f'Status code: {response.status_code}')
        soup = BeautifulSoup(response.content, 'html.parser')
        urls = soup.find_all(attrs=attrs)
        for url in urls:
            camp_sites_dc = {
                'NAME': url.text,
                'URL': url['href'],
                'PAGE_QUERY': page,
                'DT': time.strftime('%m-%d-%Y %H:%M:%S')
                }
            camp_sites.append(camp_sites_dc)
        time.sleep(SLEEP_TIME)
    return camp_sites


if __name__ == "__main__":
    BASE_URL = "https://www.fs.usda.gov/visit/destinations" +\
        "?field_rec_activities_target_id=11905&" +\
        "field_rec_forest_target_id=All&page="
    HEADERS = {'User-Agent': 'Camping Tripper/0.0.1'}
    OUTPUT_PATH = "data/camp_site_urls/"
    OUTPUT_FILE = "camp_site_urls.csv"
    STARTING_PAGE = 0
    SLEEP_TIME = 5
    first_page_url = BASE_URL+str(STARTING_PAGE)
    ending_page = scrape_ending_page()
    camp_sites = scrape_urls()
    df = pd.DataFrame(camp_sites)
    df.index.name = 'ID'
    dt_str_path = create_date_str_path()
    full_output_path = OUTPUT_PATH+dt_str_path
    if not os.path.exists(full_output_path):
        os.mkdir(full_output_path)
    df.to_csv(full_output_path+OUTPUT_FILE)
