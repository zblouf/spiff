# -*- coding: utf_8 -*-

# spiff, a python-based framework
# Copyright (c) 2006-2020, Romain Gaches, <romain@ssji.net>
#

DEFAULT_CHARSET = "utf-8"

class WebPage:
	def __init__(title="", doctype="", charset="utf-8", css_list=[], script_list=[]):
		self.title=title
		self.doctype=doctype
		self.charset=charset
		self.css_list=css_list
		self.script_list=script_list
	# CSS
	def add_css(include_type, include_data):
		self.css_list.append(dict("type"=include_type, "data"=include_data))
	def add_css_link(css_url):
		self.add_css("link", css_url)
	def add_css_inline(css_data):
		self.add_css_link("inline", css_data)

	# Scripts
	def add_script(include_type, include_data, language, charset=DEFAULT_CHARSET):
		self.script_list.append(dict("type"=include_type, "data"=include_data, "language"=language, "charset"=charset))
	def add_script_link(script_url, language, charset=DEFAULT_CHARSET):
		self.add_script("link", script_url, language, charset)
	def add_script_inline(script_data, language, charset=DEFAULT_CHARSET):
		self.add_script("inline", script_data, language, charset)
	# JS Scripts
	def add_js_link(script_url, charset=DEFAULT_CHARSET):
		self.add_script("link", script_url, "javascript", charset)
