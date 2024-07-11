from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

def scrape_urls():
    base_url = "https://www.fs.usda.gov/visit/destinations?field_rec_activities_target_id=11905&field_rec_forest_target_id=All&page="
    headers = {'User-Agent': 'Camping Tripper/0.0.1'}
    starting_page = 0
    ending_page = 224
    output_file = 'camp_site_urls.csv'
    sleep_time = 5

    camp_sites = []

    for i in range(starting_page, ending_page+1):
        url = base_url + str(i)
        print(f'Sending GET request to {url}')
        response = requests.get(url, headers=headers)
        print(f'Status code: {response.status_code}')
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all(attrs= {'class': 'usa-link'})

        for link in links:
            camp_sites_dc = {
                'NAME': link.text,
                'URL': link['href'],
                'DT': time.strftime('%m-%d-%Y %H:%M:%S')
                }
            camp_sites.append(camp_sites_dc)
        time.sleep(sleep_time)

    df = pd.DataFrame(camp_sites) 
    df.to_csv(output_file)

if __name__ == "__main__":
    scrape_urls()
