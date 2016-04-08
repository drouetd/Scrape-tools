#!/usr/bin/env python

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
		
	bolds = soup.find_all('b')
	
	# get contact name and title
	contacts = unicode(bolds[0].parent.next_sibling)
	if re.search(r'<br/>', contacts):
		# two contacts
		firstmatch = re.compile("^.*>(.*)<br/>")
		secondmatch = re.compile("(.*)</td>")
		match1 = re.search(firstmatch, contacts).group(1)
		#print "match1:", match1
		separated = split_name_and_title(match1)
		record['contact1'] = separated[0]
		record['title1'] = separated[1]
		
		match2 = re.search(secondmatch, contacts).group(1)
		#print "match2:", match2
		separated = split_name_and_title(match2)
		record['contact2'] = separated[0]
		record['title2'] = separated[1]
	else:
		separated = split_name_and_title(bolds[0].parent.next_sibling.string)
		record['contact1'] = separated[0]
		record['title1'] = separated[1]
	
	# get phone
	phone = bolds[1].parent.next_sibling.string
	record['phone'] = phone.strip()
	
	# get fax
	fax = bolds[2].parent.next_sibling.string
	record['fax'] = fax.strip()
	
	# get email
	email = bolds[3].parent.next_sibling.string
	record['email'] = email.strip()
	
	# get website
	website = bolds[4].parent.next_sibling.string
	record['website'] = website.strip()
	
	# description
	description = list(bolds[6].next_siblings)
	record['description'] = description[3].strip()
	
	# get chiffre d'affaires
	items = [unicode(x) for x in bolds]
	idx = items.index("<b>Chiffre d'affaires:</b>")
	revenues = bolds[idx].next_sibling
	record['revenues'] = revenues.strip()
	
	#print "Record:", record
	return record


def clean_name(string):
	clean = unicode(string)
	return clean[16:-8]


def split_name_and_title(string):
	nameandtitle = string.split(',')
	return [x.strip() for x in nameandtitle]



if __name__ == "__main__":
	# hack for dealing with accented text
	reload(sys)
	sys.setdefaultencoding('utf-8')
	
	# page specific setup
	companies = ["http://internet2.economie.gouv.qc.ca/Internet/aerospatiale/reperaero.nsf/bd4b8ac1bdeea6ee0525694b007576fd/b71d7e43c24254b685257b330050b1b6?OpenDocument",
				"http://internet2.economie.gouv.qc.ca/Internet/aerospatiale/reperaero.nsf/bd4b8ac1bdeea6ee0525694b007576fd/d57c1a3c1348629e85257b3200715b94?OpenDocument"]
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
