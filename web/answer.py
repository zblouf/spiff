# -*- coding: utf_8 -*-

# spiff, a python-based framework
# Copyright (c) 2006-2020, Romain Gaches, <romain@ssji.net>
#
# $Id$
#
# answer classes for web interface
# Provides generic answers

from kid import BaseTemplate, XMLSerializer, HTMLSerializer
import simplejson

__all__ = ["ExtAns", "Redirect", "Json", "File", "FileStream"]

class ExtAns:
	def __init__(self, contents):
		self.contents = contents

	def headers(self, req):
		return()

	def body(self, req):
		return self.__class__.__name__ + ": " + self.contents

class Redirect(ExtAns):
	def __init__(self, url):
		ExtAns.__init__(self, url)

	def body(self, req):
		return self.contents

class Json(ExtAns):
	def __init__(self, data, cacheable=False):
		ExtAns.__init__(self, data)
		self.cacheable = cacheable

	def headers(self, req):
		r = ("Content-Type", "text/plain"),
		if not self.cacheable:
			r += ("Cache-Control", "no-cache"),
		else:
			r += ("Cache-Control", "max-age=3600"),
		return r

	def body(self, req):
		return simplejson.dumps(self.contents, sort_keys=True, indent=4)

class File(ExtAns):
	def __init__(self, ct, path):
		ExtAns.__init__(self, path)
		self.cacheable = True
		self.ct = ct

	def headers(self, req):
		h = ("Content-Type", self.ct),
		if not self.cacheable:
			h += ("Cache-Control", "no-cache"),
		else:
			h += ("Cache-Control", "max-age=3600"),
		return h

	def body(self, req):
		fd = open(self.contents, 'r')
		r = fd.read()
		fd.close()
		return r

class FileStream(ExtAns):
	def __init__(self, ct, cont, filename=""):
		ExtAns.__init__(self, cont)
		self.filename = filename
		self.cacheable = False
		self.ct = ct

	def headers(self, req):
		h = ("Content-Type", self.ct),
		if not self.cacheable:
			h += ("Cache-Control", "no-cache"),
		else:
			h += ("Cache-Control", "max-age=3600"),
		if self.filename!="":
			h += ("Content-disposition", "attachment; filename=%s" %(self.filename.encode('latin1'))),
		return h

	def body(self, req):
		return self.contents
