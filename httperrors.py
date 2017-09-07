# Mission: Find http codes that aren't in the 200 or 300 range for all the links on a single page

import io
import requests
import string
from bs4 import BeautifulSoup

MY_SITE = "http://www.elizabethzagroba.com"
my_site_response = requests.get(MY_SITE)
page = str(BeautifulSoup(my_site_response.content, "html.parser"))
file = io.FileIO("list_of_all_links.txt", "w")

def getURL(page):
    start_link = page.find("a href")
    if start_link == -1:
        return None, 0
    start_quote = page.find('"http', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1: end_quote]
    return url, end_quote

count = 0
with open('list_of_all_links.txt', 'a') as file:
    while True: 
	    url, n = getURL(page)
	    page = page[n:]
	    if url:
	    	http_response = str(requests.head(url))
	    	if ("<Response [2" not in http_response) and ("<Response [3" not in http_response):
	    		file.write(http_response + url + '\n')
	    		count += 1
	    else:
	    	print("There are " + str(count) + " links without 200 or 300 range http responses on your site.")
	    	break
