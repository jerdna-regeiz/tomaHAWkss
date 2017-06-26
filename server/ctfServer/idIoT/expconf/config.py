#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pathlib import Path

class ExploitConfig:
	
	path = 'exploits.config.json'
	exploits = {}

	def __init__(self):
		self.read()

	def get(self, exploit, key):
		if exploit in self.exploits and key in self.exploits[exploit]:
			return self.exploits[exploit][key]
		else:
			return '';

	def put(self, exploit, key, value):
		if exploit not in self.exploits:
			self.exploits[exploit] = {}

		self.exploits[exploit][key] = value
		self.save()

	def getAll(self):
		return self.exploits.items()

	def save(self):
		with open(self.path, 'w') as outfile:
		    json.dump(self.exploits, outfile)
	
	def read(self):
		conf_file = Path(self.path)
		if conf_file.is_file():
			with open(self.path) as json_data_file:
			    self.exploits = json.load(json_data_file)
