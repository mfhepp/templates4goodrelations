#!/usr/bin/env python
# encoding: utf-8
"""
examples.py

	Python examples for using the Jinja / Django templates for GoodRelations Rich E-Commerce
	
	Also creates an RDF/XML dumpfile and a Semantic Sitemap.

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

# URIs and URI Patterns for the example shop
#
# Main page: http:/www.heppnetz.de/gr4shops/index.html
# Products pages: http:/www.heppnetz.de/gr4shops/product_<SKU>.html with <SKU> being the SKU / ProductID
# Brands page: http:/www.heppnetz.de/gr4shops/brands.html
# Bulk data URI: http:/www.heppnetz.de/gr4shops/goodrelations.rdf
# Sitemap: http:/www.heppnetz.de/gr4shops/sitemap.xml 

loader = FileSystemLoader('.')
env = Environment( loader=loader, autoescape=True, trim_blocks=True) # It is important to escape all special chars!

# ---------------------------------
# STEP 1: Populate COMPANY template
# ---------------------------------

# Example data for the company
company_data = {
	'company_name' : "Best Purchase Electronics Shop Ltd.", # Official name of the business making the offer
	'country' : "Germany",
	'language' : "en",  # ISO 639-1 code for the language of the country name, see http://en.wikipedia.org/wiki/ISO_639-1
	'city' : "Munich",
	'zip' : "12345", 
	'street' : "Example Street 123", 
	'phone' : "+49-89-6004-4217", # Must include international prefix
	'logo_uri' : "http:/www.heppnetz.de/gr4shops/logo.jpg",
	 
# The following codes are optional. Omit when in doubt.
	'duns' : "012345678", # DUNS number for the company, see
	'gln' : "1234567890123", # Global Location Number (GLN) for the company, see
	'isic' : "5610", # ISIC code for your business, see http://unstats.un.org/unsd/cr/registry/isic-4.asp
	'naics' : "722110" # North American Industry Classification System (NAICS) code for your business, see http://www.census.gov/eos/www/naics/
}

# Create RDFa snippet
template = env.get_template('template-company.html')
result = template.render(company_data, snippet=True) # populate template
r_utf8 = result.encode('UTF-8')
open("output/snippet-company.html", 'w').write(r_utf8) # write result to file

# Create complete HTML+RDFa page
title = "Website of Best Purchase Electronics Shop Ltd."
rdf_uri = "http:/www.heppnetz.de/gr4shops/goodrelations.rdf"
result = template.render(company_data, snippet=False, rdf_uri=rdf_uri, title=title) # populate template
r_utf8 = result.encode('UTF-8')
open("output/index.html", 'w').write(r_utf8) # write result to file

# ---------------------------------
# STEP 2: Populate STORES Template
# ---------------------------------

# Example data for the store
store_data = { 
	'company_uri' : "http:/www.heppnetz.de/gr4shops/index.html#company",
	'stores' : [] # will be populated below
	}
# Store in Munich
store_munich = {
	'id': "munich_store", # Short, unique identifier for the store ([a-z0-9-_]), will be hash fragment (#munich_store)
	'name' : "Best Purchase Electronics Munich Store", # Short label for the store
	'description' : "Our Munich store is the best in town ... ", # Longer text describing the store
	'language' : "en",  # ISO 639-1 code for the language of all textual elements
	'country' : "Germany",
	'city' : "Munich",
	'zip' : "12345", 
	'street' : "Example Street 123", 
	'phone' : "+49-89-6004-4217", # Must include international prefix
	'logo_uri' : "http:/www.heppnetz.de/gr4shops/munich_shop.jpg", # Logo or image URI
	'lat' : "48.08", # Geo position of the store: Latitude
	'long' : "11.64", # Geo position of the store: Longitude
	'gln' : "1234567890123", # Global Location Number (GLN) for the store (optional)
	'opening_hours' : [] # will be populated below for readability
}

# Opening Hours
mon_fri = {
'opens' : "08:00:00", # must be xsd:time format including seconds!
'closes' : "18:00:00", # must be xsd:time format including seconds!
'days' : ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], # Must be spelt EXACTLY as shown
# These will be expanded to GoodRelations URIs like http://purl.org/goodrelations/v1#Monday 
'valid_from' : "2010-01-01T00:00:00Z",
'valid_through' : "2010-12-31T23:59:59Z"
}
sat = {
'opens' : "08:00:00", # must be xsd:time format including seconds!
'closes' : "18:00:00", # must be xsd:time format including seconds!
'days' : ["Saturday"] # Must be spelt EXACTLY as shown
}
store_munich['opening_hours'] = [mon_fri, sat]
store_data['stores'] = [store_munich] # Add additional stores if needed

# Create RDFa snippet
template = env.get_template('template-stores.html')
result = template.render(store_data, snippet=True) # populate template
r_utf8 = result.encode('UTF-8')
open("output/snippet-stores.html", 'w').write(r_utf8) # write result to file

# Create complete HTML+RDFa page
title = "Best Purchase Electronics: List of Stores"
company_name = "Best Purchase Electronics Shop Ltd." 
rdf_uri = "http:/www.heppnetz.de/gr4shops/goodrelations.rdf"
result = template.render(store_data, snippet=False, rdf_uri=rdf_uri, 
	title=title, company_name=company_name) # populate template
r_utf8 = result.encode('UTF-8')
open("output/stores.html", 'w').write(r_utf8) # write result to file

# --------------------------------
# STEP 3: Populate BRANDS Template
# --------------------------------

# Example data for the brands listed in your shop
canon = {
	'name' : "canon", # Short identifier (for URI fragment - no spaces, no special characters)
	'company_name' : "Canon Europe Ltd.", # Official name
	'logo_uri' : "http:/www.heppnetz.de/gr4shops/canon.jpg", # URI of manufacturer's logo
	'uri' : "http://www.canon.com/" # URI of the manufacturer's official Web page
}

ibm = {
	'name' : "ibm", # Short identifier (for URI fragment - no spaces, no special characters)
	'company_name' : "International Business Machines Inc.", # Official name
	'logo_uri' : "http:/www.heppnetz.de/gr4shops/ibm.jpg", # URI of manufacturer's logo
	'uri' : "http://www.ibm.com/" # URI of the manufacturer's official Web page
}

brand_data =  {'brands': [canon, ibm]}
template = env.get_template('template-brands.html')

# Create RDFa snippet
result = template.render(brand_data, snippet=True) # populate template
r_utf8 = result.encode('UTF-8')
open('output/snippet-brands.html', 'w').write(r_utf8) # write result to file

# Create complete HTML+RDFa page
title = "Best Purchase Electronics: List of Brands in Our Store"
company_name = "Best Purchase Electronics Shop Ltd."
rdf_uri = "http:/www.heppnetz.de/gr4shops/goodrelations.rdf"
result = template.render(brand_data, snippet=False, rdf_uri=rdf_uri, 
	title=title, company_name=company_name) # populate template
r_utf8 = result.encode('UTF-8')
open('output/brands.html', 'w').write(r_utf8) # write result to file


# -----------------------------------------------
# STEP 4: Populate PRODUCT / OFFER Template 
# -----------------------------------------------

# Product & Offer: Canon Rebel T2i for EUR 899 incl. VAT
product_data = {
	'product_short' : "Canon Rebel T2i (EOS 550D)", # short product text
	'product_long' : """The Rebel T2i EOS 550D is Canon's top-of-the-line consumer digital SLR camera.
It can shoot up to 18 megapixel resolution photos and features an ISO range of 100-6400.""", # long product text
	'language' : "en", # ISO 639-1 code for the language of the text, see http://en.wikipedia.org/wiki/ISO_639-1
	'company_uri' : "http:/www.heppnetz.de/gr4shops/index.html#company",  # Semantic URI of the company
	# This is the URI of the page that contains the company markup (STEP 1) 
	# plus the hash fragment ("#company") used in the company_template.html file
	# In this example, http:/www.heppnetz.de/gr4shops/index.html#company"

	'product_uri' : "http:/www.heppnetz.de/gr4shops/product-canon_eos550D-kit.html", 
	# The URI of the page that will contain this snippet
	# Such is not needed for generating the snippet, but for the creation of the data dump later on.
	'business_function' : "http://purl.org/goodrelations/v1#Sell", # We offer the item for SALE
	'currency' : "EUR", # ISO 4217 standard (3 characters): USD, GBP, ...
	'price' : "899.00", # Amount
	'vat' : "true", # Value-added tax included
	'delivery_options' : [], # Will be populated below for readability
	'valid_from' : "2010-05-01T00:00:00Z", # use current date and time 
	'valid_through' : "2010-05-07T23:59:59Z", # use current date and time + 1...7 days
	'eligible_regions' : ["DE","AT","CH"], # ISO 3166-1 alpha-2 country or ISO 3166-2 region codes indicating the regions for which the offer is valid.
					  # Examples "US" for the United States, "US-AZ" for Arizona, or "DE-BY" for Bavaria
	'payment_methods' : ["http://purl.org/goodrelations/v1#PayPal", "http://purl.org/goodrelations/v1#MasterCard"], 
	# Accepted methods of payment; use GoodRelations URIs
	# Complete list at http://purl.org/goodrelations/v1#PaymentMethod
	'product_image_uri' : "http://www.heppnetz.de/gr4shops/eos550d.jpg", # Product image URI
	'product_thumbnail_uri' : "http://www.heppnetz.de/gr4shops/eos550d_small.jpg", # Product thumbnail URI
	'ean' : "013803123784", # EAN-13, 13-digit UPC, or 13-digit ISBN code for the product.
	'gtin14' : "0013803123784", # Global Trade Item Number (GTIN-14) for the product. Leave empty when in doubt.
	'sku' : "CANON_EOS550D-KIT", # Store oder brand-specific identifier ("stock keeping unit"). Can be simply your internal ID for the item.

	'stock_unit' : "C62", # UN CEFACT Unit of Measurement Code for the inventory level. Default is C62 for "piece, item"
	'stock_level' : "9", # Lower bound of current inventory level
	
	# Semantic Web URIs. Omit when in doubt.
	'manufacturer_uri' : "http:/www.heppnetz.de/gr4shops/brands.html#canon", # Semantic URI of the manufacturer
	'consumable_uris': ["http:/www.heppnetz.de/gr4shops/product_canon_battery.html#product"], # Semantic URI of consumables
	'accessory_uris' : ["http:/www.heppnetz.de/gr4shops/product_canon_bag.html#product"], # Semantic URI of accessories
	'datasheet_uri' : "http://openean.kaufkauf.net/id/EanUpc_001380303863" # Semantic link to product make and model dataset ("semantic datasheet")
}

# Create RDFa snippet for the minimal version
product_data['delivery_options'] = [{'method_uri' : "http://purl.org/goodrelations/v1#FederalExpress"}] # minimal info about delivery options

template = env.get_template('template-product.html')
result = template.render(product_data, snippet=True, minimal=True) # populate template
r_utf8 = result.encode('UTF-8')
open('output/snippet-product-canon_eos550D-kit-mini.html', 'w').write(r_utf8) # write result to file

# Create richer variant, including shipping charges etc.

# Shipment: 10 EUR including VAT for delivery via FedEx to Germany
fedex = {
	'charge' : "10.00", # Amount
	'currency' : "EUR", # ISO 4217 standard (3 characters): USD, GBP, ...
	'method_uri' : "http://purl.org/goodrelations/v1#FederalExpress", 
	'region' : "de", # Two-character version of ISO 3166-1 (ISO 3166-1 alpha-2) for countries or ISO 3166-2 for states
	'vat': "true" # Value-added tax included
}
product_data['delivery_options'] = [fedex]

# Create RDFa snippet
template = env.get_template('template-product.html')
result = template.render(product_data, snippet=True, minimal=False) # populate template
r_utf8 = result.encode('UTF-8')
open('output/snippet-product-canon_eos550D-kit.html', 'w').write(r_utf8) # write result to file

# Create Full HTML+RDFa page
title = "Best Purchase Electronics: Canon Rebel T2i (EOS 550D)"
rdf_uri = "http:/www.heppnetz.de/gr4shops/goodrelations.rdf"
company_name = "Best Purchase Electronics Shop Ltd."
result = template.render(product_data, snippet=False, minimal=False, rdf_uri=rdf_uri, 
	title=title, company_name=company_name) # populate template
r_utf8 = result.encode('UTF-8')
open('output/product-canon_eos550D-kit.html', 'w').write(r_utf8) # write result to file

#--------------------------------------------------------
# STEP 5: PRODUCT with features
# Same as STEP4, but we now use a vocabulary / ontology to 
# describe the PRODUCT / OFFER in more detail 
#--------------------------------------------------------

# Product Model: Canon Rebel T2i (EOS 550D)
product_data2 = {
	'product_short' : "Canon Rebel T2i (EOS 550D)", # short product text
	'product_long' : """The Rebel T2i EOS 550D is Canon's top-of-the-line consumer digital SLR camera.
It can shoot up to 18 megapixel resolution photos and features an ISO range of 100-6400.""", # long product text
	'language' : "en", # ISO 639-1 code for the language of the text, see http://en.wikipedia.org/wiki/ISO_639-1
	'company_uri' : "http:/www.heppnetz.de/gr4shops/index.html#company",  # Semantic URI of the company
	'product_uri' : "http:/www.heppnetz.de/gr4shops/product-canon_eos550D-kit-full.html", 
	# The URI of the page that will contain this snippet
	# Such is not needed for generating the snippet, but for the creation of the data dump later on.
	'business_function' : "http://purl.org/goodrelations/v1#Sell", # We offer the item for SALE
	'currency' : "EUR", # ISO 4217 standard (3 characters): USD, GBP, ...
	'price' : "899.00", # Amount
	'vat' : "true", # Value-added tax included
	'delivery_options' : [], # Will be populated below for readability
	'valid_from' : "2010-05-01T00:00:00Z", # use current date and time 
	'valid_through' : "2010-05-07T23:59:59Z", # use current date and time + 1...7 days
	'eligible_regions' : ["DE","AT","CH"], # ISO 3166-1 alpha-2 country or ISO 3166-2 region codes indicating the regions for which the offer is valid.
					  # Examples "US" for the United States, "US-AZ" for Arizona, or "DE-BY" for Bavaria
	'payment_methods' : ["http://purl.org/goodrelations/v1#PayPal", "http://purl.org/goodrelations/v1#MasterCard"], 
	# Accepted methods of payment; use GoodRelations URIs
	# Complete list at http://purl.org/goodrelations/v1#PaymentMethod
	
	'product_image_uri' : "http://www.heppnetz.de/gr4shops/eos550d.jpg", # Product image URI
	'product_thumbnail_uri' : "http://www.heppnetz.de/gr4shops/eos550d_small.jpg", # Product thumbnail URI
	'ean' : "013803123784", # EAN-13, 13-digit UPC, or 13-digit ISBN code for the product.
	'gtin14' : "0013803123784", # Global Trade Item Number (GTIN-14) for the product. Leave empty when in doubt.
	'sku' : "CANON_EOS550D-KIT", # Store oder brand-specific identifier ("stock keeping unit"). Can be simply your internal ID for the item.

	'stock_unit' : "C62", # UN CEFACT Unit of Measurement Code for the inventory level. Default is C62 for "piece, item"
	'stock_level' : "9", # Lower bound of current inventory level

	# Semantic Web URIs. Omit when in doubt.
	'manufacturer_uri' : "http:/www.heppnetz.de/gr4shops/brands.html#canon", # Semantic URI of the manufacturer
	'consumable_uris': ["http:/www.heppnetz.de/gr4shops/products_canon_battery.html#product"], # Semantic URI of consumables
	'accessory_uris' : ["http:/www.heppnetz.de/gr4shops/products_canon_bag.html#product"], # Semantic URI of accessories

	# Ontology-based description of technical features
	# Prefix and URI for the vocabulary/ies to be used
	'prefixes' : [{	'ns_prefix' : "ceo", # Consumer Electronics Ontology
					'ns_uri' : "http://www.ebusiness-unibw.org/ontologies/consumerelectronics/v1#"}],
	# Specify class URI for product type
	'product_class_uri' : "http://www.ebusiness-unibw.org/ontologies/consumerelectronics/v1#DigitalCamera",
	'features' : [] # we populate that list in a second step for readability
}

product_data2['delivery_options'] = [fedex]
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
product_data2['features'] = [digital_zoom, video_res, display, weight, focal_length]

# Create complete HTML+RDFa page
title = "Best Purchase Electronics: Canon Rebel T2i (EOS 550D)"
rdf_uri = "http:/www.heppnetz.de/gr4shops/goodrelations.rdf"
company_name = "Best Purchase Electronics Shop Ltd."
result = template.render(product_data2, snippet=False, minimal=False, rdf_uri=rdf_uri, 
	title=title, company_name=company_name) # populate template
r_utf8 = result.encode('UTF-8')
open('output/product-canon_eos550D-kit-full.html', 'w').write(r_utf8) # write result to file

# --------------------------------
# STEP 6: Create Data Dump in RDF
# --------------------------------

# Important: When using HTML templating APIs or simple string operations for creating
# the RDF/XML dump file, make sure you properly encode special characters like <,>, &, '
# In this example, this has been done by "autoescape=True" in the statement
# env = Environment( loader=loader, autoescape=True)

template = env.get_template('template-rdf.rdf')
rdf_data = {
	'company_data' : company_data, 
	'product_data' : [product_data,product_data2], # List of ALL products in your shop
	'brand_data' : brand_data, 
	'store_data' : store_data,
	'company_page' : "http:/www.heppnetz.de/gr4shops/index.html",
	'brands_page' : "http:/www.heppnetz.de/gr4shops/brands.html",
	'stores_page' : "http:/www.heppnetz.de/gr4shops/stores.html",
	# Prefix and URI for the vocabulary/ies to be used
	'prefixes' : [{'ns_prefix' : "ceo", 'ns_uri' : "http://www.ebusiness-unibw.org/ontologies/consumerelectronics/v1#"}],
	# For the RDF/XML template, those are defined globally and you MUST use the prefixes consistently accross all products and datasheet.
}

result = template.render(rdf_data, minimal=False) # populate template
r_utf8 = result.encode('UTF-8')
open('output/goodrelations.rdf', 'w').write(r_utf8) # write result to file

# --------------------------------
# STEP 7: Write Sitemap
# --------------------------------

# Important: When using HTML templating APIs or simple string operations for creating
# the XML sitemap file, make sure you properly encode special characters like <,>, &, '
# In this example, this has been done by "autoescape=True" in the statement
# env = Environment( loader=loader, autoescape=True)

template = env.get_template('template-sitemap.xml')

sitemap_data = {
	'uris' : [], # List with all "regular" HTML pages, will be populated later
	'label' : "GoodRelations RDF Data Dump for http://www.heppnetz.de/gr4shops/",
	'rdf_uri' : "http://www.heppnetz.de/gr4shops/goodrelations.rdf", # URI of the RDF data dump file
	'rdf_example_product' : "http://www.heppnetz.de/gr4shops/product-canon_eos550D-kit.html", # URI of one product page
	'rdf_example_company' : "http://www.heppnetz.de/gr4shops/index.html",  # URI of the company page
	'rdf_example_brand' : "http://www.heppnetz.de/gr4shops/brands.html", # URI of the brand page (or one example page, if you have multiple)
	'rdf_example_store' : "http://www.heppnetz.de/gr4shops/stores.html", # URI of the stores page (or one example page, if you have multiple)
	'rdf_example_datasheet' : "http://www.heppnetz.de/gr4shops/product-canon_eos550D-kit.html",# URI of one datasheet page 
	'rdf_changefreq' : "daily" # Typical change frequency of the RDF/XML data dump
	}

# Compile a list of all company, product item, and brand URIs
pages = ['http:/www.heppnetz.de/gr4shops/index.html',
		'http:/www.heppnetz.de/gr4shops/brands.html',
		'http:/www.heppnetz.de/gr4shops/stores.html',
		'http:/www.heppnetz.de/gr4shops/product-canon_eos550D-kit.html',
		'http:/www.heppnetz.de/gr4shops/datasheet-canon_eos550D-kit.html'
		# Add URIs of all shop item pages here
		# ...
		]

for uri in pages:
	sitemap_data['uris'].append(dict(uri=uri,lastmod="2010-05-28",changefreq="daily", priority="0.5"))
	# 'lastmod' : "2010-05-28", # Date of last change on the page
	# 'changefreq' : "daily" # Typical change frequency for that page

result = template.render(sitemap_data)
# write result to file
r_utf8 = result.encode('UTF-8')
open('output/sitemap.xml', 'w').write(r_utf8)

print "All files have been created successfully."

