# -*- coding: utf-8 -*-
import json

import requests

from monitoring import Monitoring


class Gru:
    def __init__(self):
        self.minions = []
        self.monitor = None

    def start_monitoring_local(self):
        # monitoring lokal in thread starten
        if self.monitor is None:
            self.monitor = Monitoring()
            self.monitor.start()
            return True
        else:
            return False

    def start_monitoring_remote(self, remote):
        # TODO Monitoring mithilfe von salt auf minion starten
        return False

    def stop_monitoring_local(self):
        self.monitor.stop()

    def stop_monitoring_remote(self, remote):
        requests.get("http://{}:5000/stop".format(remote))

    def add_regex_local(self, regex):
        # einen neuen regelären ausdruck für den lokalen monitor hinzufügen
        self.monitor.regs.append(regex)

    def add_regex_remote(self, remote, regex):
        # einen neuen regelären ausdruck für den remote monitor hinzufügen
        requests.post("http://{}:5000/add_regex".format(remote), data={'regex': regex})

    def remove_regex_local(self, regex):
        self.monitor.remove_regex(regex)

    def remove_regex_remote(self,remote, regex):
        requests.post("http://{}:5000/del_regex".format(remote), data={'regex': regex})

    def list_regex_local(self):
        return self.monitor.regs

    def list_regex_remote(self, remote):
        response = requests.get("http://{}:5000/list_regex".format(remote))
        return json.loads(response.content)

    def get_events(self):
        events = []
        if self.monitor is not None:
            events.append(self.monitor.get_events_dict())


        for minion in self.minions:
            response = requests.get("http://{}:5000/get_events".format(minion))
            events.append(json.loads(response.content))
        # events von allen aktiven monitor instanzen abfragen

        return events