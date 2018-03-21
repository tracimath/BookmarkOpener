#!/usr/bin/env/python3
#1 python3
# FreeTextbooks.py - Accepts the name of the textbook as a command-line argument
# and downloads a PDF of the textbook to the user's computer.

# IN PROGRESS: Need to create a check to ensure that the file format is indeed
# a PDF. Some links end in ".pdf" but are not true PDFs.
# Ensure that the program looks at more than just the first page of Google
# search results, if necessary.

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

        # Parse the text to retrieve just the link
        s = string.find("q=") + 2
        e = string.find(".pdf") + 4
        final_link = string[s:e]
        final_link = final_link.replace('25', '')
        # Shorten the file so that it consists of all of the content after
        # that comes after this link
        string = string[e:]

        # Fetch the PDF with the link and check the validity of the link
        pdf_req = requests.get(final_link)
        pdf_req.raise_for_status()
        # Open PDF and check the number of pages
        local_file = open('some_file.pdf', 'wb+')
        local_file = local_file.write(pdf_req.content)

        print(final_link)

        # Test whether the file is truly a PDF, continue with the next
        # link if the file is not a PDF
        error = 0

        try:
            reader = PyPDF2.PdfFileReader(open('some_file.pdf', 'rb'))
        except PyPDF2.utils.PdfReadError:
            error = 1
            print("invalid PDF file")

        if error == 1:
            continue

        pages = reader.getNumPages()
        # Check whether the number of pages exceeds 10
        if pages > 10:
            name = textbook_name + " Textbook.pdf"
            os.rename('some_file.pdf', name)
            count = count + 1
        else:
            # Add code to delete the PDF from the user's computer
            continue
