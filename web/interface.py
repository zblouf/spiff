# -*- coding: utf_8 -*-

# spiff, a python-based framework
# Copyright (c) 2006-2020, Romain Gaches, <romain@ssji.net>
#
# $Id$
#
# Generic classes for web interface
# Provides Request and Answer classes and some http-headers related utilities
#

import os
from Cookie import SimpleCookie
from kid import BaseTemplate, XMLSerializer, HTMLSerializer

class Request:
	"""
	"""
	def __init__(  self,
	               transhost,
	               uri,
	               peer,
	               path_info,
	               cookies,
	               ans_class,
	               config=None):
		# path_info must be checked & modified to ensure that its final value
		# is the same whatever the web server & CGI interface are
		#   heading and trailing slashes are removed
		if path_info == '/':
			path_info = ''
		if len(path_info) > 0:
			if path_info[0] == '/':
				path_info = path_info[1:]
			if path_info[-1] == '/':
				path_info = path_info[:-1]
		self.path_info = path_info

		self.form = {}

		# path_info is splitted into a list which will be passed to further handlers
		self.path_list = self.path_info.split('/')
		self.path_length = len(self.path_list)

		if uri[-1] == '/':
			uri = uri[:-1]

		self.remote = peer
		self.base_url = transhost
		self.self_url = transhost + uri
		parent = os.path.dirname(uri)
		if parent == '/':
			parent = ''
		self.parent_dir = transhost + parent

		self.cookie = SimpleCookie()
		if cookies:
			self.cookie.load(cookies)

		self.answer = ans_class(self)

		# Config
		if config is not None:
			self.config = config

		# base_url & path_list correction
		try:
			if self.config.base_url_suffix != "":
				self.base_url = self.base_url + "/" + self.config.base_url_suffix
				if self.path_list[0] == self.config.base_url_suffix:
					self.path_list = self.path_list[1:]
		except:
			pass

		# Logging

		# Session
		if self.config.session['autoload'] == True:
			from spiff.session import generic as session
			#_cookie_name = self.config.session["cookie_name"]
			_cookie_name = self.config.session['cookie_name']
			if _cookie_name in self.get_cookie_fields():
				_sid = self.get_cookie_field(_cookie_name, '')
				self.sess = session.Session(self, _sid, self.config.session['driver'])
			else:
				self.sess = session.Session(self, None, self.config.session['driver'])

		# Temporary Datastore declaration
		self.data = dict()

	#
	# Temporary Datastore functions
	#

	# Elements of this temporary datastore are only kept as the current request
	# goes on. They'll be flushed right after the answer.
	def set_data(self, key, value):
		self.data[key] = value

	def get_data(self, key, default_value=""):
		if self.data.has_key(key):
			return self.data[key]
		else:
			return default_value

	def drop_data(self, key):
		if self.data.has_key(key):
			del self.data[key]


	#
	# Cookie managing
	#
	def get_cookies(self):
		"Returns the raw cookie object."
		return self.cookie

	def get_cookie_fields(self):
		"Returns the list of cookies keys."
		return self.cookie.keys()

	def get_cookie_field(self, name, default_value=None):
		"Returns value of the 'name' cookie."
		try:
			return self.cookie[name].value
		except:
			return default_value

	def get_cookie_dict(self):
		"Returns cookies in a key/value dictionnary."
		cookie_dict = {}
		for field in self.get_cookie_fields():
			cookie_dict[field] = self.get_cookie_field(field)
		return cookie_dict

	#
	# Forms
	#
	def get_form_field(self, name, default_value=None):
		"Returns data contained in 'name' form field."
		try:
			return self.form[name].value
		except:
			try:
				return self.form[name]
			except:
				return default_value

	def get_form_fields(self):
		"Returns the list of form fields."
		_form = {}
                for _field in self.form:
                    _form[_field] = self.form[_field].value
                return _form


class Answer:
	def __init__(self, req):
		self.cookie = None
		self.req = req
		self.headers = []
		self.res = ""

	def set_cookie(self, name, val=None):
		if self.cookie is None:
			self.cookie = SimpleCookie()
		self.cookie[name] = val
		try:
			self.cookie[name]["Max-Age"] = self.req.config.session.default_life
		except:
			self.cookie[name]["Max-Age"] = 3600
		try:
			self.cookie[name]["Path"] = self.req.config.session["cookie"]["path"]
		except:
			print "Content-type: text/html"
			print ""
			print "cookie path error !"
		try:
			self.cookie[name]["Domain"] = self.req.config.cookie["domain"]
		except:
			pass
		try:
			self.cookie[name]["Comment"] = self.req.config.cookie["comment"]
		except:
			pass

	def set_cookie_dict(self, cookie_dict):
		for cookie in cookie_dict:
			self.set_cookie(cookie, cookie_dict[cookie])

	def destroy_cookie(self, name):
		if self.cookie is None:
			self.cookie = SimpleCookie()
		self.cookie[name] = ''
		self.cookie[name]["Max-Age"] = 0

	def send_cookies(self):
		self.req.write(self.cookie.output())
		self.req.write('\n')

	def do_html_template(self, tmpl):
		ct = 'text/html'
		tmpl.req = self.req
		serializer = HTMLSerializer(
			doctype = ("HTML", "-//W3C//DTD HTML 4.01//EN",
		               "http://www.w3.org/TR/html4/strict.dtd"))
		h = ('Content-Type', ct),
		h += ('Cache-Control', 'no-cache'),
		return h, tmpl.serialize(output=serializer)

	def do_django_template(self, tmpl, ctxt = {}):
		ct = 'text/html; charset=UTF-8'
		tmpl.request = self.req
		h = ('Content-Type', ct),
		h += ('Cache-Control', 'no-cache'),
		return h, tmpl.render(ctxt).encode('utf-8')

def parse_accept_language(http_accept_language):
	"Parses HTTP_ACCEPT_LANGUAGE header and returns a list of language dictionnaries"
	languages = []
	raw_strings = http_accept_language.split(',')
	for raw_string in raw_strings:
		lang_params = raw_string.split(';')
		parsed_tempo = {}
		if len(lang_params) > 0:
			parsed_tempo['locale'] = lang_params[0]
		if len(lang_params) > 1:
			param = lang_params[1]
			if param.count("q=") <> 0:
				order = param.split('=')
				parsed_tempo['order'] = order[1]
		languages.append(parsed_tempo)
	return languages
