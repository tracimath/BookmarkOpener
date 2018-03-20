#1 python3
# mapIt.py - Imports the bookmarks from the Chrome browser and opens them
# all at once as separate tabs in a new browser
# ./BookmarksOpener.py <- fetches Chrome bookmarks
# ./BookmarksOpener.py bookmarks.html 3
# ./BookmarksOpener.py bookmarks.html
# Second command-line argument specifies number of bookmarks to be opened,
# Default number of bookmarks is 5

import webbrowser, sys
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import json
import os

if len(sys.argv) == 1:
    webbrowser.open(chrome://bookmarks/)

# Checks for second command line argument specifying number of links to open
if len(sys.argv) > 2:
    n = sys.argv[2]
else:
    n = 5

if len(sys.argv) > 1:
    # Open html file of links from command line for reading
    bookmark_links = str(sys.argv[1])
    # parse html
    f = open(bookmark_links, "r")
    f_links = open("links.txt", "w+")

    for link in BeautifulSoup(f, 'html.parser', parseOnlyThese=SoupStrainer('a')):
        if link.has_attr('href'):
            f_links.write(link['href'] + "\n")

    f_links = open("links.txt", "r")

# Read the strings in the html and open them in Chrome browser
f2 = f_links.readlines()
count = 0;
for x in f2:
    if count > n:
        break;
    # Remove the new line character and open links in same browser
    x = x.rstrip()
    webbrowser.open(url = str(x), new = 2)
    count = count + 1

# Close the files
f.close()
f_links.close()
