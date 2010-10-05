#!/usr/bin/env python
# encoding: utf-8
"""
notify.py

Python examples of notifying Semantic Web crawlers of GoodRelations rich e-commerce meta-data

URIs for the example shop:

Bulk data URI: http:/www.heppnetz.de/gr4shops/goodrelations.rdf
Sitemap: http:/www.heppnetz.de/gr4shops/sitemap.xml 

Created by Martin Hepp on 2010-05-28.
"""

import sys
import os
import urllib

EMAIL = "mhepp@computer.org" # Insert your e-mail address (for receiving Sindice status info)

# --------------------------------
# STEP: Notifying Search Engines
# --------------------------------

# Important: You must FIRST upload the sitemap.xml and goodrelations.rdf files to their 
# official locations, e.g.
#
# http://www.heppnetz.de/gr4shops/goodrelations.rdf
# and
# http:/www.heppnetz.de/gr4shops/sitemap.xml

# STEP 1: Notify Ping The Semantic Web
# See http://pingthesemanticweb.com/api.php
# Technique: HTTP GET or POST

PTSW_URL = 'http://pingthesemanticweb.com/rest/' # REST (much faster, less traffic per request)
rdf_uri = "http://www.heppnetz.de/gr4shops/goodrelations.rdf" # URI of the dump file

print "Registering data dump file at Ping The Semantic Web"
try:
	params = urllib.urlencode({'url': rdf_uri})
	u = PTSW_URL+"?"+params
	response = urllib.urlopen(u)
	print response.read()
#	print "HTTP Status Code: %s" % response.getcode() # requires Python 2.6x
	headers = response.info()
	print 'HEADERS :'
	print headers
	response.close()
except:
    print "ERROR:", sys.exc_info()[0]

# STEP 2: Notify Sindice of Semantic Sitemap
# See http://sindice.com/api/v1/sitemap
# Technique: HTTP POST only
import urllib

SINDICE_URI = "http://sindice.com/api/v1/sitemap"
sitemap_uri = "http:/www.heppnetz.de/gr4shops/sitemap.xml" 
email = EMAIL # E-mail address of site owner or web master; optional
# If an email address is provided, then Sindice will send you a message when your dataset has been indexed.

print "Registering Semantic Sitemap at Sindice"
try:
	params = urllib.urlencode({'url' : sitemap_uri, 'email' : email})
	response = urllib.urlopen(SINDICE_URI, params)
	print response.read()
#	print "HTTP Status Code: %s" % response.getcode() # requires Python 2.6x
	headers = response.info()
	print 'HEADERS :'
	print headers
	response.close()
except:
    print "ERROR:", sys.exc_info()[0]
