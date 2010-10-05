#!/usr/bin/env python
# encoding: utf-8
"""
shop-vocabulary.py

	Python examples for using the Jinja / Django templates for GoodRelations Rich E-Commerce
	
	This template shows how to expose the product categories and features for a specific shop
	in order to describe products much more precisely.
	
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
# STEP 1: Creating a shop-specific GoodRelations Vocabulary
# ==================================================

loader = FileSystemLoader('.')
env = Environment(loader=loader, autoescape=True, trim_blocks=True)
env.trim_blocks=True 

# It is important that special characters are properly escaped in the resulting markup! ( e.g. & as &amp; etc.)

# --------------------------------------------------
# Master data for the company
# --------------------------------------------------
base_uri = 'http:/www.heppnetz.de/gr4shops/shop-vocabulary.html'
language = "en" # ISO 639-1 code for the language of the class and property labels, see http://en.wikipedia.org/wiki/ISO_639-1
company_data = {
	'company_name' : "Best Purchase Electronics Shop Ltd.", # Official name of the business making the offer

	'license' : "Insert terms or conditions for using this page or URI of standard license - e.g. Creative Commons" 
}

# --------------------------------------------------
# Products or services categories
# --------------------------------------------------
categories = [
# Top-level Category - Clothing
	{
		'id' : "clothing", # short identifier for the product category (avoid special chars)
		'label' : "Clothing and Accessories", # name of the category
		'image_uri': "http:/www.heppnetz.de/gr4shops/images/clothing.png" # URI of an image for the category (optional)
		# no supercategory_id, because this is the top-level category
	},
# T-Shirts
	{
		'id' : "tshirts",
		'label' : "T-Shirts and related products", 
		'image_uri': "http:/www.heppnetz.de/gr4shops/images/tshirts.png",
		'supercategory_id' : "clothing", # The ID of the parent category, if it exists.
		# Note: The prefix C_ will be added by the template.
	},
# Accessories
	{
		'id' : "accessories",
		'label' : "Ties and Accessories", 
		'image_uri': "http:/www.heppnetz.de/gr4shops/images/accessories.png",
		'supercategory_id' : "clothing" 
	}
]

# --------------------------------------------------
# Quantitative ("numerical") features for products
# Use this pattern for features that refer to a quantitative measurement, e.g.
# screen diameter, weight, seating capacity, operating voltage, etc. 
# Note: You can always safely use text features (see below) as a fall-back option if unsure.
# However, this reduces the market visibility of your data.
# --------------------------------------------------

quantitative_properties = [
# Weight
	{
		'id' : "weight",
		'label' : "Net weight of the product"
		# Note: The unit of measurement will be determined when describing an actual product
	},
# Operating temperature
	{
		'id' : "operating_temp",
		'label' : "Recommended operating temperature (can be a point value or interval)"
		# Note: The unit of measurement will be determined when describing an actual product
	}	
]

# --------------------------------------------------
# Textual features for products
# Use this pattern for all features that hold textual values and that you cannot represent in a more granular way, e.g.
# color or maintenance instructions
# If you have a small, controlled set of allowed values, it is better to use qualitative properties
# and to predefine all allowed values.
# --------------------------------------------------
text_properties = [
# Color
	{
		'id' : "color",
		'label' : "Color of the product"	
	},
# Care Instructions
	{
		'id' : "care_instructions",
		'label' : "Care and maintenance instructions for the product"	
	}
]

# --------------------------------------------------
# Boolean features for products
# Use this pattern for all features that hold yes/no values 
# --------------------------------------------------

boolean_properties = [
# All-weather
	{
		'id' : "all_weather",
		'label' : "Suited for all-weather use"	
	}
]
# --------------------------------------------------
# Qualitative properties, values, and value classes
# --------------------------------------------------

qualitative_properties = [
# Material
	{
		'id' : "material",
		'label' : "Main material of the product"	
	},
	{
		'id' : "garment_size",
		'label' : "Garment size for T-Shirts and Sweaters"	
	}
]

# --------------------------------------------------
# Value Classes
# --------------------------------------------------
value_classes = [
# Shirt Size (S, M, L, XL, XXL)
	{
		'id' : "shirt_sizes",
		'label' : "Garment sizes for shirts and sweaters"	
	},
# Materials (Leather, Cotton, Synthetics)
	{
		'id' : "material_types",
		'label' : "Material types for products"	
	}
]

# --------------------------------------------------
# Values
# --------------------------------------------------
values = [
# Shirt Sizes (S, M, L, XL, XXL)
# Example of ordered values
	{
		'id' : "S",
		'label' : "Garment size: Small (S)",	
		'class_id' : "shirt_sizes", # The ID of the value type
		'lesser' : "M", # The ID of the next greater value 
		# 'greater' : None # The ID of next smaller value
	},
	{
		'id' : "M",
		'label' : "Garment size: Medium (M)",	
		'class_id' : "shirt_sizes", # The ID of the value type
		'lesser' : "L", # The ID of the next greater value 
		'greater' : "S" # The ID of next smaller value
	},
	{
		'id' : "L",
		'label' : "Garment size: Large (L)",	
		'class_id' : "shirt_sizes", # The ID of the value type
		'lesser' : "XL", # The ID of the next greater value 
		'greater' : "M" # The ID of next smaller value
	},
	{
		'id' : "XL",
		'label' : "Garment size: Extra Large (XL)",	
		'class_id' : "shirt_sizes", # The ID of the value type
		'lesser' : "L", # The ID of the next greater value 
		'greater' : "XL" # The ID of next smaller value
	},
	{
		'id' : "XXL",
		'label' : "Garment size: XXL",	
		'class_id' : "shirt_sizes", # The ID of the value type
		# 'lesser' : None, # The ID of the next greater value 
		'greater' : "XL" # The ID of next smaller value
	},
# Materials (Leather, Cotton, Synthetics)
# Example of unordered values
	{
		'id' : "leather",
		'label' : "Material: Genuine Leather",	
		'class_id' : "material_types" # The ID of the value type
	},
	{
		'id' : "cotton",
		'label' : "Material: Cotton",	
		'class_id' : "material_types" # The ID of the value type
	},
	{
		'id' : "synthetics",
		'label' : "Material: Synthetics",	
		'class_id' : "material_types" # The ID of the value type
	}
]

template = env.get_template('template-shop_vocabulary.html')

data = {'base_uri' : base_uri, 'language': language,'company_data' : company_data, 
	'categories' : categories,
	'quantitative_properties' : quantitative_properties, 
	'text_properties' : text_properties,
	'boolean_properties' : boolean_properties, 
	'qualitative_properties' : qualitative_properties, 
	'value_classes' : value_classes,
	'values' : values}

result = template.render(data) # populate template
	
r_utf8 = result.encode('UTF-8')
open("output/shop-vocabulary.html", 'w').write(r_utf8) # write result to file

#--------------------------------------------------------
# STEP 2: Using the vocabulary for describing a PRODUCT
#--------------------------------------------------------

# Example data for one product and the delivery options + charges

# Shipment: 10 EUR including VAT for delivery via FedEx to Germany
fedex = {
	'charge' : "10.00", # Amount
	'currency' : "EUR", # ISO 4217 standard (3 characters): USD, GBP, ...
	'method_uri' : "http://purl.org/goodrelations/v1#FederalExpress", 
	'region' : "de", # Two-character version of ISO 3166-1 (ISO 3166-1 alpha-2) for countries or ISO 3166-2 for states
	'vat': "true" # Value-added tax included
}

# Product & Offer: GoodRelations T-Shirt Size XXL for EUR 8.99 incl. VAT
product_data = {
	'product_short' : "GoodRelations T-Shirt Size XXL", # short product text
	'product_long' : """GoodRelations T-Shirt Size XXL""", # long product text
	'language' : "en", # ISO 639-1 code for the language of the text, see http://en.wikipedia.org/wiki/ISO_639-1
	'company_uri' : "http:/www.heppnetz.de/gr4shops/index.html#company",  # Semantic URI of the company who is making the offer
	# This is the URI of the page that contains the company markup (STEP 1) 
	# plus the hash fragment ("#company") used in the company_template.html file
	# In this example, http:/www.heppnetz.de/gr4shops/index.html#company"

	'product_uri' : "http:/www.heppnetz.de/gr4shops/product_goodrelations-tshirt.html", 
	# The URI of the page that will contain this snippet
	# Such is not needed for generating the snippet, but for the creation of the data dump later on.
	'business_function' : "http://purl.org/goodrelations/v1#Sell", # We offer the item for SALE
	'currency' : "EUR", # ISO 4217 standard (3 characters): USD, GBP, ...
	'price' : "8.99", # Amount
	'vat' : "true", # Value-added tax included
	'delivery_options' : [fedex] ,
	'valid_from' : "2010-05-01T00:00:00Z", # use current date and time 
	'valid_through' : "2010-05-07T23:59:59Z", # use current date and time + 1...7 days
	'eligible_regions' : ["DE","AT","CH"], # ISO 3166-1 alpha-2 country or ISO 3166-2 region codes indicating the regions for which the offer is valid.
					  # Examples "US" for the United States, "US-AZ" for Arizona, or "DE-BY" for Bavaria
	'payment_methods' : ["http://purl.org/goodrelations/v1#PayPal", "http://purl.org/goodrelations/v1#MasterCard"], 
	# Accepted methods of payment; use GoodRelations URIs
	# Complete list at http://purl.org/goodrelations/v1#PaymentMethod
	
	'product_image_uri' : "http:/www.heppnetz.de/gr4shops/gr-tshirt.jpg", # Product image URI
	'product_thumbnail_uri' : "http:/www.heppnetz.de/gr4shops/gr-tshirt_small.jpg", # Product thumbnail URI
	'ean' : "013803123784", # EAN-13, 13-digit UPC, or 13-digit ISBN code for the product.
	'gtin14' : "0013803123784", # Global Trade Item Number (GTIN-14) for the product. Leave empty when in doubt.
	'sku' : "GRTSHIRT-XXL", # Store oder brand-specific identifier ("stock keeping unit"). Can be simply your internal ID for the item.

	'stock_unit' : "C62", # UN CEFACT Unit of Measurement Code for the inventory level. Default is C62 for "piece, item"
	'stock_level' : "2", # Lower bound of current inventory level
	# HERE STARTS THE ONTOLOGY-BASED PART
	# Prefix and URI for the vocabulary to be used (we must use a prefix for our vocab in RDFa 1.0)
	'prefixes' : [{	'ns_prefix' : "shop", # Consumer Electronics Ontology
					'ns_uri' : "http:/www.heppnetz.de/gr4shops/shop-vocabulary.html#"}],
	# Specify class URI for product type
	'product_class_uri' : "http:/www.heppnetz.de/gr4shops/shop-vocabulary.html#C_tshirts",
	'features' : [] # we populate that list in a second step for readability
}
# Defining semantic properties

# Quantitative Properties
weight = {
	'type' : "quantitative",
	'uri' : "shop:P_weight", # this expands to
	# http:/www.heppnetz.de/gr4shops/shop-vocabulary.html#P_weight - RDFa 1.0 quirk
	'value' : "280",
	'unit_code' : "GRM", # Unit: gram (use UN/CEFACT common code)
	'datatype' : "float" # only "float" and "integer" are supported
	}
operating_temperature = {
	'type' : "quantitative",
	'uri' : "shop:P_operating_temp",
	'min_value' : "5",
	'max_value' : "45",
	'unit_code' : "CEL", # Unit: degree Celsius (use UN/CEFACT common code)
	'datatype' : "float"
	}
# Text Properties
color = {
	'type' : "text",
	'uri' : "shop:P_color",
	'value' : "ocean blue",
	'language' : "en" # ISO 639-1 code for the language of the text, see http://en.wikipedia.org/wiki/ISO_639-1
}
# Boolean Properties
all_weather = {
	'type' : "boolean",
	'uri' : "shop:P_all_weather",
	'value' : "true" # true or false
}
#Qualitative Properties
size = {
	'type' : "qualitative",
	'uri' : "shop:P_garment_size",
	'value_uri' : "http:/www.heppnetz.de/gr4shops/shop-vocabulary.html#V_XXL" # Must be a full URI - RDFa 1.0 quirk
}
material = {
	'type' : "qualitative",
	'uri' : "shop:P_material",
	'value_uri' : "http:/www.heppnetz.de/gr4shops/shop-vocabulary.html#V_cotton" # Must be a full URI - RDFa 1.0 quirk
}

# Add list of features to the product data dict
product_data['features'] = [weight, operating_temperature, color, all_weather, size, material]

# Create Full HTML+RDFa page
template = env.get_template('template-product.html')
title = "Best Purchase Electronics: GoodRelations T-Shirt XXL"
rdf_uri = "http:/www.heppnetz.de/gr4shops/goodrelations.rdf"
company_name = "Best Purchase Electronics Shop Ltd."
result = template.render(product_data, snippet=False, minimal=False, rdf_uri=rdf_uri, 
	title=title, company_name=company_name) # populate template
r_utf8 = result.encode('UTF-8')
open('output/product_goodrelations-tshirt.html', 'w').write(r_utf8) # write result to file

print "All files have been created successfully."
