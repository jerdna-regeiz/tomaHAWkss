#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
class WorkerConfig:
	
	workers = {'worker1': 'best worker'}

	def getAll(self):
		return self.workers.items()

	def save(self):
		serialized = json.dumps(self.workers)
		#TODO: save in file
