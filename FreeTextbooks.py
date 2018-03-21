#!/usr/bin/env/python3
#1 python3
# FreeTextbooks.py - Accepts the name of the textbook as a command-line argument
# and downloads a PDF of the textbook to the user's computer.

import webbrowser, sys, requests, PyPDF2, os
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

# All command-line arguments after the program name are interpreted as part
# of the name of the textbook
if len(sys.argv) > 1:
    textbook_name = ' '.join(sys.argv[1:])
else:
    print("Error: Must enter name of textbook.")
    sys.exit()

# Search Google for the textbook
keyword = 'https://www.google.com/search?hl=en&q=' + textbook_name + " textbook pdf"

# Fetch the page of the Google search results
res = requests.get(keyword)
res.raise_for_status()
text = res.text

# Parse the html page with beautifulSoup
soup = BeautifulSoup(text, "html.parser")

# Count is needed to print just the first result
count = 0
for link in soup.find_all("a"):
    if count == 0 and (".pdf") in str(link) and "github.com" not in str(link):
        string = str(link)

        s = string.find("q=") + 2
        e = string.find(".pdf") + 4
        final_link = string[s:e]
        final_link = final_link.replace('25', '')
        string = string[e:]

        pdf_req = requests.get(final_link)
        pdf_req.raise_for_status()
        local_file = open('some_file.pdf', 'wb+')
        local_file = local_file.write(pdf_req.content)
        #open PDF and check the number of pages
        print(final_link)

        error = 0

        try:
            reader = PyPDF2.PdfFileReader(open('some_file.pdf', 'rb'))
        except PyPDF2.utils.PdfReadError:
            error = 1
            print("invalid PDF file")

        if error == 1:
            continue

        pages = reader.getNumPages()

        if pages > 10:
            name = textbook_name + " Textbook.pdf"
            os.rename('some_file.pdf', name)
            count = count + 1
        else:
            continue
