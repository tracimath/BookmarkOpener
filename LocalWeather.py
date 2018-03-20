#!/usr/bin/env/python3
#1 python3
# LocalWeather.py - Launches a map in the browser using an address from the
# command line or clipboard.

import webbrowser, sys, requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

# Use ipinfo.io website to fetch information about user's location
res = requests.get('http://ipinfo.io/json')
print(res.status_code == requests.codes.ok)
text = res.text

# Parse the city and region from the page
city_s = text.find("city")
city_e = text[city_s:].find(",") + city_s
city = text[city_s+7:city_e]
text = text[city_e+1:]
region_e = text.find(",")
region_s = text.find(": ")
region = text[region_s+2:region_e]

# Remove quotations from strings for city and region
city = city.replace('"', '')
region = region.replace('"', '')

# Search for "city" "region" weather and store page in object
keyword = 'https://www.google.com/search?hl=en&q=' + city + " "+ region + " weather"
search_results = requests.get(keyword)
print(res.status_code == requests.codes.ok)

# Parse the html page with beautifulSoup
soup = BeautifulSoup(search_results.content, "lxml")
# Count is needed to print just the first result
count = 0
for link in soup.select(".r a"):
    if count == 0:
        # Parse for search result link
        string = str(link)
        s = string.find("q=") + 2
        e = string[s+1+5:].find(":") + 1 + 5 + s
        final_link = string[s:e]
        print(s)
        print(e)
        print(final_link)
        # Open search result link and add 1 to count
        webbrowser.open(final_link)
        count = count + 1
