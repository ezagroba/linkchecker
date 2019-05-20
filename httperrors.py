# Mission: Find http codes that aren't in the 200 or 300 range for all the links on a single page

import os
import errno
import http
import requests
import ssl
import string
import urllib.request
from bs4 import BeautifulSoup
from bs4 import SoupStrainer


MY_SITE = "http://www.elizabethzagroba.com"
my_site_response = requests.get(MY_SITE)
only_external_links = SoupStrainer(target="_blank")
page = str(BeautifulSoup(my_site_response.content, "html.parser", parse_only=only_external_links))


def get_url(website):
	start_link = website.find("a href")
	if start_link == -1:
		return None, 0
	start_quote = website.find('"http', start_link)
	end_quote = website.find('"', start_quote + 1)
	stripped_url = website[start_quote + 1: end_quote]
	return stripped_url, end_quote


try:
	os.remove('list_of_all_links.txt')
except OSError:
	pass

count = 0
with open('list_of_all_links.txt', 'a') as file:
	while True: 
		url, n = get_url(page)
		page = page[n:]
		if url:
			try:
				req = urllib.request.urlopen(url)
			except urllib.error.URLError as explanation:
				file.write(str(explanation) + " " + url + '\n')
				count += 1
		else:
			print("There are " + str(count) + " links outside of the 200 or 300 range of http responses on your site.")
			break
