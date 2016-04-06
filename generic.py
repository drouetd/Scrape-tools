#!/usr/bin/env python

import sys
import re
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def page_html(url=None):
	"""
	Returns the html for the member list page of Aeromtl
	"""
	
	driver = webdriver.PhantomJS()
	driver.get(url)
	
	# retrieve the desired page
	try:
		WebDriverWait(driver, 2)
		html = driver.page_source
	except:
		print "%s occurred." % (sys.exc_info()[0].__name__)
		return
	finally:
		driver.quit()
	return html

def parse_aero(soup):
	membership = []
	
	mask = re.compile("member\d+")
	
	members = soup.find_all('div', id=mask, limit=None)
	print "%d members found." % len(members)
	for m in members:
		member ={}
		# get name
		member['name'] = m.h2.string
		#print member['name']
		
		# get contact info
		infos = m.find('div', class_='list-info')
		data = infos.find_all('div')
		for d in data:
			if d.find('span', class_='icon1'):
				member['phone'] = d.p.string
				#print member['phone']
			if d.find('span', class_='icon3'):
				member['email'] = d.p.string
				#print member['email']
			if d.find('span', class_='icon4'):
				member['website'] = d.p.string
				#print member['website']
		
		# add record to the list
		membership.append(member)
		#print membership
		
	return membership


if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding('utf-8')
	page_url = "http://www.aeromontreal.ca/member-list.html?count=184#member5"
	page = page_html(page_url)
	if page:
		contact_list = parse_aero(BeautifulSoup(page, 'html5lib'))
		
	#for contact in contact_list:
		#print contact['name']
		#print contact['phone']
		#print contact['email']
		#print contact['website']
		#print'\n'
		
	with open('aero.csv', 'wb') as csvfile:
		fieldnames = ['name', 'phone', 'email', 'website']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';',quotechar='"',quoting=csv.QUOTE_ALL)
		writer.writeheader()
		for contact in contact_list:
			try:
				writer.writerow(contact)
			except:
				print "%s occurred with %s" % (sys.exc_info()[0].__name__, contact['name'])
				print contact
				print'\n'