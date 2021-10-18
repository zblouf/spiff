# -*- coding: utf_8 -*-

# spiff, a python-based framework
# Copyright (c) 2006-2020, Romain Gaches, <romain@ssji.net>

import cgi
import os
import sys
from Cookie import SimpleCookie

from django.template import Template, loader, Context

import interface

__all__ = ['Request']

class Request(interface.Request):
	def __init__(self, _config=None):
		port = os.getenv('SERVER_PORT')

		url_port = ""
		if os.getenv('HTTPS') == "on":
			method = 'https://'
			if port != "443":
				url_port = ':' + str(port)
		else:
			method = 'http://'
			if port != "80":
				url_port = ':' + str(port)

		base = method + str(os.getenv('SERVER_NAME')) + url_port

		#_config = config

		interface.Request.__init__(
			self,
			transhost = base,
			uri = str(os.getenv('SCRIPT_NAME')),
			peer = str(os.getenv('REMOTE_ADDR')),
#			path_info = str(os.getenv('PATH_INFO')),
			path_info = str(os.getenv('SCRIPT_NAME')),
#			path_info = str(os.getenv('REQUEST_URI')),
			cookies = os.getenv('HTTP_COOKIE'),
			ans_class = Answer,
			config = _config)
			#)

		self.form = cgi.FieldStorage()
		self.languages = interface.parse_accept_language(str(os.getenv('HTTP_ACCEPT_LANGUAGE')))

		self.http_user_agent = os.getenv('HTTP_USER_AGENT')
		self.sess.set_data('user_agent', os.getenv('HTTP_USER_AGENT'))

	def write(self, data):
		sys.stdout.write(data)

class Answer(interface.Answer):
	def __call__(self, ans, ctxt = None):
		from answer import BaseTemplate, ExtAns, Redirect
		if isinstance(ans, BaseTemplate):
			headers, res = self.do_html_template(ans)
		if isinstance(ans, ExtAns):
			headers = ans.headers(self.req)
			res = ans.body(self.req)
			if isinstance(ans, Redirect):
				if ':' in res[:8]:
					url = res
				else:
					url = self.req.base_url + '/'+res
				headers = ('Location', url),
				res = "Moved"
		self.headers = headers
		self.res = res

	def send(self):
		self.req.sess.save()
		print '\r\n'.join(map(': '.join, self.headers))
		if self.cookie:
			print self.cookie
		print ""
		print self.res
