#!/usr/bin/env python
# encoding: utf-8
"""
simple.py

	Python examples for using the Jinja / Django templates for GoodRelations Rich E-Commerce
	
	Written by Martin Hepp, http://www.heppnetz.de/.
	All templates and code samples are available under LPGL. Attribution kindly requested.
		
	Wiki: http://www.ebusiness-unibw.org/wiki/GoodRelationsTemplates
	GoodRelations: http://purl.org/goodrelations/

	(C) 2010 Martin Hepp, Universitaet der Bundeswehr Muenchen, Germany
	http://www.unibw.de/ebusiness/
"""

import sys
import os
# ----------------------------------------------------
# COMPANY Page
# ----------------------------------------------------
# Example data
company_data = {
	'company_name' : "Best Purchase Electronics Shop Ltd.", # Official name of the business making the offer
	'country' : "Germany",
	'language' : "en",  # ISO 639-1 code for the language of the country name, see http://en.wikipedia.org/wiki/ISO_639-1
	'city' : "Munich",
	'zip' : "12345", 
	'street' : "Example Street 123", 
	'phone' : "+49-89-6004-4217", # Must include international prefix
	'logo_uri' : "http:/www.heppnetz.de/gr4shops/logo.jpg"
}

from jinja2 import *
loader = FileSystemLoader('.')
env = Environment( loader=loader, autoescape=True, trim_blocks=True)
template = env.get_template('template-company.html')

# OPTION 1: Create full HTML+RDFa page
title = "Website of Best Purchase Electronics Shop Ltd."
html = template.render(company_data, snippet=False, title=title) # populate template
html = html.encode('UTF-8')
print html

# OPTION 2: Create and insert a RDFa snippet
static_html = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML+RDFa 1.0//EN" "http://www.w3.org/MarkUp/DTD/xhtml-rdfa-1.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" version="XHTML+RDFa 1.0" xml:lang="en">
<head>
	<title>My page</title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
</head>
<body>
<p>Demo page</p>
</body>
</html>
"""

# Create RDFa snippet
snippet = template.render(company_data, snippet=True) # populate template
snippet = snippet.encode('UTF-8')

# Insert the snippet just before the closing <body> element.
html = static_html.replace("</body>", snippet+"</body>")
print html



# ---------------------------------------------
# PRODUCT: Create complete HTML+RDFa page 
# ---------------------------------------------

# Product & Offer: Canon Rebel T2i for EUR 899 incl. VAT
product_data = {
	'product_short' : "Canon Rebel T2i (EOS 550D)", # short product text
	'product_long' : """The Rebel T2i EOS 550D is Canon's top-of-the-line consumer digital SLR camera.""", 
	'language' : "en", # ISO 639-1 code for the language of the text
	'company_uri' : "http:/www.heppnetz.de/gr4shops/index.html#company", 
	# This is the URI of the page that contains the company markup 
	# plus the hash fragment ("#company") used in the company_template.html file
	'business_function' : "http://purl.org/goodrelations/v1#Sell", 
	'currency' : "EUR", # ISO 4217 standard (3 characters): USD, GBP, ...
	'price' : "899.00", # Amount
	'vat' : "true", # Value-added tax included
	'delivery_options' : [], # Will be populated below for readability
	'valid_from' : "2010-05-01T00:00:00Z", # use current date and time 
	'valid_through' : "2010-05-07T23:59:59Z", # use current date and time + 1...7 days
	'eligible_regions' : ["DE","AT","CH"], # ISO 3166-1 alpha-2
	'payment_methods' : ["http://purl.org/goodrelations/v1#PayPal", "http://purl.org/goodrelations/v1#MasterCard"], 
	# Accepted methods of payment; use GoodRelations URIs
	# Complete list at http://purl.org/goodrelations/v1#PaymentMethod
	'product_image_uri' : "http://www.heppnetz.de/gr4shops/eos550d.jpg", # Product image URI
	'product_thumbnail_uri' : "http://www.heppnetz.de/gr4shops/eos550d_small.jpg", # Product thumbnail URI
	'ean' : "013803123784", # EAN-13, 13-digit UPC, or 13-digit ISBN code for the product.
	'sku' : "CANON_EOS550D-KIT" # Store oder brand-specific identifier ("stock keeping unit"). Can be simply your internal ID for the item.
}

fedex = {'method_uri' : "http://purl.org/goodrelations/v1#FederalExpress"}
product_data['delivery_options'] = [fedex]

template = env.get_template('template-product.html')

# Create RDFa snippet
html = template.render(product_data, snippet=False, minimal=True) # populate template
html = html.encode('UTF-8')
print html

