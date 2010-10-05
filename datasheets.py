#!/usr/bin/env python
# encoding: utf-8
"""
datasheets.py

	Python examples for using the Jinja / Django templates for GoodRelations Rich E-Commerce
	
	This template shows how to expose the datasheets, i.e. technical feature data for commodities.

	Also, it demonstrates the usage of external ontologies for product classes and features.
	
	Written by Martin Hepp, http://www.heppnetz.de/.
	All templates and code samples are available under LPGL. Attribution kindly requested.
		
	Wiki: http://www.ebusiness-unibw.org/wiki/GoodRelationsTemplates
	GoodRelations: http://purl.org/goodrelations/

	(C) 2010 Martin Hepp, Universitaet der Bundeswehr Muenchen, Germany
	http://www.unibw.de/ebusiness/
"""

import sys
import os
from jinja2 import *

# URIs and URI Patterns for the example shop:
#
# Main page: http:/www.heppnetz.de/gr4shops/index.html
# Products pages: http:/www.heppnetz.de/gr4shops/product_<SKU>.html with <SKU> being the SKU / ProductID
# Brands page: http:/www.heppnetz.de/gr4shops/brands.html
# Bulk data URI: http:/www.heppnetz.de/gr4shops/goodrelations.rdf
# Sitemap: http:/www.heppnetz.de/gr4shops/sitemap.xml 
#
# Vocabulary page: http:/www.heppnetz.de/gr4shops/shop-vocabulary.html
# Product Class: http:/www.heppnetz.de/gr4shops/shop-vocabulary.html#C_<id>
# Product Property: http:/www.heppnetz.de/gr4shops/shop-vocabulary.html#P_<id>
# Value Class: http:/www.heppnetz.de/gr4shops/shop-vocabulary.html#VC_<id>
# Property Value: http:/www.heppnetz.de/gr4shops/shop-vocabulary.html#V_<id>

# ==================================================
# STEP 1: Semantic Datasheet
# ==================================================

loader = FileSystemLoader('.')
env = Environment(loader=loader, autoescape=True, trim_blocks=True)
# It is important that special characters are properly escaped in the resulting markup! ( e.g. & as &amp; etc.)

# Datasheet / Product Model: Canon Rebel T2i (EOS 550D)
datasheet_data = {
	'product_short' : "Canon Rebel T2i (EOS 550D)", # short product text
	'product_long' : """The Rebel T2i EOS 550D is Canon's top-of-the-line consumer digital SLR camera.""", # long product text
	'language' : "en", # ISO 639-1 code for the language of the text, see http://en.wikipedia.org/wiki/ISO_639-1
	'datasheet_uri' : "http:/www.heppnetz.de/gr4shops/datasheet-canon_eos550D-kit.html", 
	# The URI of the page that will contain this snippet. Only needed for the RDF/XML dump.

	'product_image_uri' : "http://www.heppnetz.de/gr4shops/eos550d.jpg", # Product image URI
	'product_thumbnail_uri' : "http://www.heppnetz.de/gr4shops/eos550d_small.jpg", # Product thumbnail URI
	'ean' : "013803123784", # EAN-13, 13-digit UPC, or 13-digit ISBN code for the product.
	'gtin14' : "0013803123784", # Global Trade Item Number (GTIN-14) for the product. Leave empty when in doubt.
	'sku' : "CANON_EOS550D-KIT", # Store oder brand-specific identifier ("stock keeping unit"). Can be simply your internal ID for the item.

	# OPTIONAL: Semantic Web URIs. Omit when in doubt.
	'manufacturer_uri' : "http:/www.heppnetz.de/gr4shops/brands.html#canon", # Semantic URI of the manufacturer
	'variant_of_uri' : "http:/www.heppnetz.de/gr4shops/datasheet-canon_eos550-series.html#datasheet", # Semantic link to baseline product
	'consumable_uris': ["http:/www.heppnetz.de/gr4shops/datasheets_canon_battery.html#datasheet"], # Semantic URI of consumables
	'accessory_uris' : ["http:/www.heppnetz.de/gr4shops/datasheets_canon_bag.html#datasheet"], # Semantic URI of accessories
	'related_datasheets_uris' : ["http:/www.heppnetz.de/gr4shops/datasheet-canon_eos550D-maxikit.html#datasheet"],
	'predecessor_uris' : ["http:/www.heppnetz.de/gr4shops/datasheet-canon_eos440D.html#datasheet"],
	'successor_uris' : ["http:/www.heppnetz.de/gr4shops/datasheet-canon_eos660D.html#datasheet"],

	# Ontology-based description of technical features
	# You can also create a brand-specific vocabulary, see shop-vocabulary.py
	# Prefix and URI for the vocabulary/ies to be used
	'prefixes' : [{	'ns_prefix' : "ceo", # Consumer Electronics Ontology
					'ns_uri' : "http://www.ebusiness-unibw.org/ontologies/consumerelectronics/v1#"}],
	# Specify class URI for product type
	'product_class_uri' : "http://www.ebusiness-unibw.org/ontologies/consumerelectronics/v1#DigitalCamera",
	'features' : [] # we populate that list in a second step for readability
}

# Defining semantic properties
# The type of the property is determined by the products ontology that you use!
# See http://www.ebusiness-unibw.org/ontologies/consumerelectronics/v1 for this example

# Boolean Property: Digital zoom: yes
digital_zoom = {
	'type' : "boolean",
	'uri' : "ceo:hasDigitalZoom",
	'value' : "true" # true or false
}
# Text Property: Video resolution 1024x768 pixels
video_res = {
	'type' : "text",
	'uri' : "ceo:hasVideoResolution",
	'value' : "1024x768 pixels",
	'language' : "en" # ISO 639-1 code for the language of the text, see http://en.wikipedia.org/wiki/ISO_639-1
}
# Qualitative Property: Display Type: LCD
display = {
	'type' : "qualitative",
	'uri' : "ceo:hasDisplayType",
	'value_uri' : "http://www.ebusiness-unibw.org/ontologies/consumerelectronics/v1#LCD" # Must be a full URI - RDFa 1.0 quirk
}
# Quantitative Properties
# Weight: 280 gram
weight = {
	'type' : "quantitative",
	'uri' : "ceo:hasWeight", 
	'value' : "280",
	'unit_code' : "GRM", # Unit: gram (use UN/CEFACT common code)
	'datatype' : "float" # only "float" and "integer" are supported
	}
#Focal length range: 20-120 mm
focal_length = {
	'type' : "quantitative",
	'uri' : "ceo:hasFocalLength",
	'min_value' : "20",
	'max_value' : "120",
	'unit_code' : "MMT", # Unit: mm (use UN/CEFACT common code)
	'datatype' : "float"
	}

# Add list of features to the product data dict
datasheet_data['features'] = [digital_zoom, video_res, display, weight, focal_length]

# Create RDFa snippet
template = env.get_template('template-datasheet.html')
result = template.render(datasheet_data, snippet=True) # populate template
r_utf8 = result.encode('UTF-8')
open('output/snippet-datasheet-canon_eos550D-kit.html', 'w').write(r_utf8) # write result to file

# Create Full HTML+RDFa page
template = env.get_template('template-datasheet.html')
title = "Best Purchase Electronics: Datasheet for the Canon EOS 550D KIT "
rdf_uri = "http:/www.heppnetz.de/gr4shops/datasheets.rdf"
company_name = "Best Purchase Electronics Shop Ltd."
result = template.render(datasheet_data, snippet=False, rdf_uri=rdf_uri, 
	title=title, company_name=company_name) # populate template
r_utf8 = result.encode('UTF-8')
open('output/datasheet-canon_eos550D-kit.html', 'w').write(r_utf8) # write result to file

# --------------------------------
# STEP 2: Create Data Dump for Datasheets in RDF
# --------------------------------

# Important: When using HTML templating APIs or simple string operations for creating
# the RDF/XML dump file, make sure you properly encode special characters like <,>, &, '
# In this example, this has been done by "autoescape=True" in the statement
# env = Environment( loader=loader, autoescape=True)

datasheet_data['datasheet_uri'] = "http:/www.heppnetz.de/gr4shops/datasheet-canon_eos550D-kit.html"
# Example data for the company

# Example data for the brands listed in your shop
canon = {
	'name' : "canon", # Short identifier (for URI fragment - no spaces, no special characters)
	'company_name' : "Canon Europe Ltd.", # Official name
	'logo_uri' : "http:/www.heppnetz.de/gr4shops/canon.jpg", # URI of manufacturer's logo
	'uri' : "http://www.canon.com/" # URI of the manufacturer's official Web page
}
brand_data =  {'brands': [canon]}
brands_page = "http:/www.heppnetz.de/gr4shops/brands.html" # URI of the page containing the brands data

template = env.get_template('template-rdf.rdf')
rdf_data = {
	'datasheet_data' : [datasheet_data], # List of ALL datasheets in your shop
	'brand_data' : brand_data,
	'brands_page' : brands_page,
	'prefixes' : [{'ns_prefix' : "ceo", 'ns_uri' : "http://www.ebusiness-unibw.org/ontologies/consumerelectronics/v1#"}]
	# For the RDF/XML template, those are defined globally and you MUST use the prefixes consistently accross all products and datasheets.
}
result = template.render(rdf_data) # populate template
r_utf8 = result.encode('UTF-8')
open('output/datasheets.rdf', 'w').write(r_utf8) # write result to file

print "All files have been created successfully."