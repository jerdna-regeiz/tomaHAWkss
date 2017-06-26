#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pathlib import Path

class TargetConfig:
	
	path = 'targets.config.json'
	targets = {}

	def __init__(self):
		self.read()

	def get(self, target, key):
		if target in self.targets and key in self.targets[target]:
			return self.targets[target][key]
		else:
			return '';

	def put(self, target, key, value):
		if target not in self.targets:
			self.targets[target] = {}

		self.targets[target][key] = value
		self.save()

	def getAll(self):
		return self.targets.items()

	def save(self):
		with open(self.path, 'w') as outfile:
		    json.dump(self.targets, outfile)
	
	def read(self):
		conf_file = Path(self.path)
		if conf_file.is_file():
			with open(self.path) as json_data_file:
			    self.targets = json.load(json_data_file)

def main():
	conf = TargetConfig()
	conf.put("172.11.11.11", "user", "root")
	print(conf.get("172.11.11.11", "user"))
	print("\n")
	print(conf.getAll())

if __name__ == "__main__":
    main()
