# -*- coding: utf-8 -*-

import sys
import re
from bs4 import BeautifulSoup
from utils import get_html, write_to_csv

def parse_aero(raw_html):
	""" Extracts membership list from Aero Montreal website """
	
	# setup
	soup = BeautifulSoup(raw_html, 'html5lib')
	membership = []
	mask = re.compile("member\d+")
	
	# parse!
	members = soup.find_all('div', id=mask, limit=None)
	print "%d members found." % len(members)
	for m in members:
		member ={}
		# get name
		member['name'] = m.h2.string
		
		# get contact info
		infos = m.find('div', class_='list-info')
		data = infos.find_all('div')
		for d in data:
			if d.find('span', class_='icon1'):
				member['phone'] = d.p.string
			if d.find('span', class_='icon3'):
				member['email'] = d.p.string
			if d.find('span', class_='icon4'):
				member['website'] = d.p.string
		
		# add record to the list
		membership.append(member)
		
	return membership


if __name__ == "__main__":

	# page specific setup
	page_url = ""
	output_filename = 'Data/aero.csv'
	fields = []

	# hack for dealing with accented text
	reload(sys)
	sys.setdefaultencoding('utf-8')

	# read single page and extract data
	html = get_html(page_url)
	if html:
		record_list = parse_aero(html)
		print record_list

	# write records to csv
	write_to_csv(output_filename, fields, record_list)

