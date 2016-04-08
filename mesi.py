# -*- coding: utf-8 -*-

import sys
import re
from bs4 import BeautifulSoup
from generic import get_html
from generic import write_to_csv

def parse_mesi_company_page(raw_html):
	""" Parses the info from a company page. """
	
	record = {'contact2':'', 'title2': ''}
	soup = BeautifulSoup(raw_html, 'html5lib')
	
	# get company name
	name = soup.find_all('font', size="5")
	if name:
		record['name'] = clean_name(name)
		print "Name:", record['name']
		
	bolds = soup.find_all('b')
	items = [unicode(x) for x in bolds]
	
	# get contact name and title
	contacts = unicode(bolds[0].parent.next_sibling)
	if re.search(r'<br/>', contacts):
		# two contacts
		firstmatch = re.compile("^.*>(.*)<br/>")
		secondmatch = re.compile("(.*)</td>")
		match1 = re.search(firstmatch, contacts).group(1)
		separated = split_name_and_title(match1)
		record['contact1'] = separated[0]
		if len(separated) > 1:
			record['title1'] = separated[1]
		
		match2 = re.search(secondmatch, contacts).group(1)
		separated = split_name_and_title(match2)
		record['contact2'] = separated[0]
		if len(separated) > 1:
			record['title2'] = separated[1]
	else:
		separated = split_name_and_title(bolds[0].parent.next_sibling.string)
		record['contact1'] = separated[0]
		if len(separated) > 1:
			record['title1'] = separated[1]
	
	# get phone
	phone = bolds[1].parent.next_sibling.string
	record['phone'] = phone.strip()
	
	# get fax
	try:
		idx = items.index("<b>Télécopieur:</b>")
		fax = bolds[idx].parent.next_sibling.string
		record['fax'] = fax.strip()
	except:
		record['fax'] = ''
		print "%s no fax for %s." % (sys.exc_info()[0].__name__, record['name'])
	
	# get email
	try:
		idx = items.index("<b>Courriel:</b>")
		email = bolds[idx].parent.next_sibling.string
		record['email'] = email.strip()
	except:
		record['email'] = ''
		print "%s no email for %s." % (sys.exc_info()[0].__name__, record['name'])
	
	# get website
	try:
		idx = items.index("<b>Site web:</b>")
		website = bolds[idx].parent.next_sibling.string
		record['website'] = website.strip()
	except:
		record['website'] = ''
		print "%s no website for %s." % (sys.exc_info()[0].__name__, record['name'])
	
	# description
	try:
		idx = items.index("<b>Domaines d'activités</b>")
		description = list(bolds[idx].next_siblings)
		record['description'] = description[3].strip()
	except:
		record['description'] = ''
		print "%s no description for %s." % (sys.exc_info()[0].__name__, record['name'])
	
	# get chiffre d'affaires
	try:
		idx = items.index("<b>Chiffre d'affaires:</b>")
		revenues = bolds[idx].next_sibling
		record['revenues'] = revenues.strip()
	except:
		record['revenues'] = ''
		print "%s no revenues for %s." % (sys.exc_info()[0].__name__, record['name'])
	
	return record


def clean_name(string):
	clean = unicode(string)
	return clean[16:-8]


def split_name_and_title(string):
	nameandtitle = string.split(',')
	return [x.strip() for x in nameandtitle]


def get_mesi_urls():
	""" Loads html containing the links to company pages. """
	
	with open("Data/a.html", 'r') as f:
		html = f.read()
		soup = BeautifulSoup(html, 'html5lib')
		links = soup.find_all('a')
		urls = ["http://internet2.economie.gouv.qc.ca" + str(link['href']) for link in links]
	
	return urls


if __name__ == "__main__":
	# hack for dealing with accented text
	reload(sys)
	sys.setdefaultencoding('utf-8')
	
	companies = get_mesi_urls()
	#sys.exit()
	
	
	# page specific setup
	"""
	companies = ["http://internet2.economie.gouv.qc.ca/Internet/aerospatiale/reperaero.nsf/bd4b8ac1bdeea6ee0525694b007576fd/905426df69f342a985257ec0002146d8?OpenDocument",
				"http://internet2.economie.gouv.qc.ca/Internet/aerospatiale/reperaero.nsf/bd4b8ac1bdeea6ee0525694b007576fd/097aeedcac7ea4de85257b3200715bc0?OpenDocument",
				"http://internet2.economie.gouv.qc.ca/Internet/aerospatiale/reperaero.nsf/bd4b8ac1bdeea6ee0525694b007576fd/c06a60a8d08182f885257b32007164cc?OpenDocument",
				"http://internet2.economie.gouv.qc.ca/Internet/aerospatiale/reperaero.nsf/bd4b8ac1bdeea6ee0525694b007576fd/11323676470757f285257b320071648b?OpenDocument"]
	"""
	record_list =[]
	
	# iterate through a list of company pages
	for company in companies:
		html = get_html(company)
		if html:
			record_list.append(parse_mesi_company_page(html))
			
	# write records to csv
	output_filename = 'Data/mesi.csv'
	fields = ['name', 'contact1', 'title1', 'contact2', 'title2','phone', 'fax', 'email', 'website', 'revenues', 'description']
	write_to_csv(output_filename, fields, record_list)
