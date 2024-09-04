# Camp Sites Project

## Name: Pilgrim // Pilgram // Voypi

## Camp Sites Links 

### Description
Collects all links from Forest Service Page:
https://www.fs.usda.gov/visit/destinations?field_rec_activities_target_id=11905&field_rec_forest_target_id=All&page=0
Then collects all links from next page.

Page from the link above is destination page, filtered to 'Campground Camping' and Forest '-Any-'.

Each link should be a "recreation destination", which is a camp site. Although some links seem to not be camp sites.


### How to Run
Activate the virtual environment and run the following command:
```pipenv shell```
```python camp_sites_links.py```

NOTE: This script will output a csv file 'camp_sites_links.csv'. Running the script again will overwrite any file of the same name.

### TO DO
- Logging
- Script always goes from page 0 to hard coded end page. Start page should always be 0, but ending page can change, and DOES. Current hard coded page is 224 and seems like there are 229 pages now.
- Create UID for each record.
- Use word URL instead of link.
- Output duration of script. 

## Camp Sites Info

### Description
Collections information from all the urls in the csv file 'camp_sites_links.csv'. Currently, information collected is the latitude and longitude, if available.

Example of a camp site page: https://www.fs.usda.gov/recarea/scnf/recarea/?recid=76056


### How to Run
Activate the virtual environment and run the following command:
```pipenv shell```
```python camp_sites_info.py <batch_start> <batch_end>```

NOTE: Batch start will be starting index from the csv file 'camp_sites_links.csv'.
Batch end will be the ending index from the csv file 'camp_sites_links.csv'.
The script will output a csv file 'camp_sites_info.csv'. Because the script runs in batches, we will not overwrite the output file. Batch end is non-inclusve, so if you want to run the script for the first 100 links, you would run:
```python camp_sites_info.py 0 100```
And, the next 100 links would be:
```python camp_sites_info.py 100 200```

### TO DO
- Add delete command to delete the csv file 'camp_sites_info.csv' before running the script.
- Ability to detect duplicates in the csv file 'camp_sites_info.csv' and report that.
- Come up with list of attributes to collect from each camp site.
    - Current list is Latitude, Longitude.
    - Additional Attributes: Fee, elevation, number of sites, National Forest, water.
- What to do if attribute is missing from a camp site page.


## Map Camp Sites

Using https://leafletjs.com/ to create map on a webpage.
look into Routing Machine Plugin for creating routes between 2 locations.

## Front-end

Steps to build and run front-end:
```
npm install
```

```
npm run build
```

Open localhost:9000 in web browser


## Useful Links
Recration.gov API: https://ridb.recreation.gov/docs
Leaflet Examples: https://tomickigrzegorz.github.io/leaflet-examples/#
Switch2OSM: https://switch2osm.org/serving-tiles/
