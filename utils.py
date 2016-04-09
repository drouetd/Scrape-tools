# -*- coding: utf-8 -*-

import sys
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

def get_html(url=None):
	""" Returns the raw html for a given url """
	
	driver = webdriver.PhantomJS()
	driver.get(url)
	
	# retrieve the desired page
	try:
		WebDriverWait(driver, 2)
		html = driver.page_source
	except:
		print "%s occurred while trying to read page." % (sys.exc_info()[0].__name__)
		return
	finally:
		driver.quit()
	return html


def write_to_csv(filename, fields, records):
	""" Writes a list of dictionaries to a csv file. """
	
	with open(filename, 'wb') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fields, delimiter=',',quotechar='"',quoting=csv.QUOTE_ALL)
		# writer.writeheader()
		for rec in records:
			try:
				writer.writerow(rec)
			except:
				print "%s occurred with %s" % (sys.exc_info()[0].__name__, rec[fields[0]])
				print rec
				print'\n'
	
	return 


