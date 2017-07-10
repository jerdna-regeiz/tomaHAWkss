# -*- coding: utf-8 -*-

import datetime
import re
from binascii import hexlify
from collections import deque
from pathlib import Path
from subprocess import Popen
from threading import Thread

import inotify.adapters


"""
Verwaltet die Lokale und Remote Monitoring Instanzen und stellt gefundene Pakete bereit
"""


class Event:
    def __init__(self, description, data, preceding_events=None):
        self.description = description
        self.data = data
        self.preceding_events = preceding_events

    def __repr__(self):
        return self.description

    def __str__(self):
        return self.description

    def hex_data(self):
        return hexlify(self.data)

    def to_dict(self):
        if self.preceding_events is not None:
            return {
                "description": self.description,
                "data": self.data,
                "preceding_events":
                [x.to_dict() for x in self.preceding_events]
            }
        else:
            return {"description": self.description, "data": self.data}


class Monitoring(Thread):
    def __init__(self, time_delta=30):
        super(Thread, self).__init__(daemon=True)

        self.regs = ["flag"]
        self.running = True

        # TODO vielleicht auf ports und ip addressen filtern
        # self.ips = []
        # self.ports = []

        self.time_delta = time_delta
        self.p = Path("/tmp/tcpflow")
        if not self.p.exists():
            self.p.mkdir()
        self.max_files = 200
        self.min_files = 100
        self.file_count = 0
        self.proc = None
        self.events = deque(maxlen=100)

    def add_regex(self, regex):
        if regex not in self.regs:
            self.regs.append(regex)

    def remove_regex(self, regex):
        try:
            self.regs.remove(regex)
            return True
        except:
            return False

    def list_regex(self):
        return self.regs

    def get_events(self):
        return list(self.events)

    def get_events_dict(self):
        return [x.to_dict() for x in self.events]

    def cleanup(self):
        packets = [x for x in self.p.iterdir() if x.is_file()]
        if len(packets) > self.max_files:
            packets.sort(key=lambda x: x.stat().st_ctime)
            for x in range(len(packets) - self.min_files):
                packets[x].unlink()
            self.file_count -= len(packets) - self.min_files

    def stop(self):
        self.running = False

    def run(self, start_tcpflow=True):
        i = inotify.adapters.Inotify()

        if start_tcpflow:
            self.proc = Popen(
                ["tcpflow", "-i", "lo", "-S", "enable_report=NO"], cwd=self.p)

        i.add_watch(b"/tmp/tcpflow")

        try:
            for event in i.event_gen():
                if not self.running:
                    break

                if event is not None:
                    (header, type_names, watch_path, filename) = event
                    if type_names[0] == "IN_CLOSE_WRITE":
                        self.file_count += 1
                        if self.file_count > self.max_files:
                            self.cleanup()
                        s = filename.decode()
                        self.scan_file(Path(s))

        finally:
            i.remove_watch(b"/tmp/tcpflow")

            if start_tcpflow:
                self.proc.kill()

    def split_filename(self, filename):
        return (filename[0:15], filename[16:21], filename[22:37],
                filename[38:43])

    def pretty_print_file(self, file, data=True):
        create_time = file.stat().st_ctime
        # print(create_time)
        print(
            datetime.datetime.fromtimestamp(create_time).strftime(
                '%Y-%m-%d %H:%M:%S'))
        print("src: {}:{}, dst: {}:{}".format(*self.split_filename(file.name)))
        if data:
            with file.open("r") as fd:
                print(fd.read())
        print("##########################")

    def create_event(self, file, preceding_events=None):
        create_time = file.stat().st_ctime
        # print(create_time)
        timestamp = datetime.datetime.fromtimestamp(create_time).strftime(
            '%Y-%m-%d %H:%M:%S')
        description = "[{}] src: {}:{}, dst: {}:{}".format(
            timestamp, *self.split_filename(file.name))

        with file.open("r") as fd:
            data = fd.read()

        return Event(description, data, preceding_events)

    def scan_file(self, file):
        with file.open("r") as fd:
            s = fd.read()
        for r in self.regs:
            if re.findall(r, s):
                print("bingo")
                # self.pretty_print_file(file)
                event = self.create_event(file)
                create_time = file.stat().st_ctime

                event_list = []
                print("suche ältere dateien")
                src = file.name[:16]
                dst = file.name[22:-5]
                for i in self.p.iterdir():
                    ctime = i.stat().st_ctime
                    if i.name != file.name:
                        if ctime < (create_time + 1) and ctime > (
                                create_time - self.time_delta):
                            if src in i.name and dst in i.name:
                                # self.pretty_print_file(i, False)
                                event_list.append(self.create_event(i))

                event = self.create_event(file, event_list)

                self.events.append(event)

