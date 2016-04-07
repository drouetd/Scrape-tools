#!/usr/bin/env python

import re
from bs4 import BeautifulSoup

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

