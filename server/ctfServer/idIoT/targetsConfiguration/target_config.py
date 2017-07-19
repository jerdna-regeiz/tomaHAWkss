#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pathlib import Path


class TargetConfig:
    path = 'targets.config.json'
    targets = {}

    def __init__(self):
        self.read()

    def get(self, targetIp, key):
        if targetIp in self.targets and key in self.targets[targetIp]:
            return self.targets[targetIp][key]
        else:
            return ''

    def put(self, targetIp, key, value):
        if targetIp not in self.targets:
            self.targets[targetIp] = {}

        self.targets[targetIp][key] = value
        self.save()

    def remove(self, targetIp):
        self.targets.pop(targetIp, None)
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
