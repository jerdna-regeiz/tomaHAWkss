# -*- coding: utf-8 -*-

from flask import Blueprint, redirect, json
from flask import request
from gru import Gru

monitoring = Blueprint('monitoring', __name__, url_prefix="/monitoring")

gru = Gru()

"""
Rest Schnittstelle für das RemoteMonitoring

Erlaubt das starten und stoppen von monitoring instanzen sowohl auf dem Server
als auch auf den minions und deren Verwaltung die das hinzufügen und entfernen von
regulären ausdrücken und das abrufen von gefundenen paketen erlaubt

Zum übergeben von Argumenten werden http-post requests verwendet mit den argumenten
remote ( adresse des minions ) und regex ( regulärer ausdruck als string ) wo nötig
"""

@monitoring.route("/start_local")
def start_local():
    if gru.start_monitoring_local():
        return ("",200)
    else:
        return ("Could not start local monitoring",500)

@monitoring.route("/start_remote",methods=['POST'])
def start_remote():
    if gru.start_monitoring_remote(request.form["remote"]):
        return("",200)
    else:
        return ("Could not start local monitoring on: {}".format(request.form["remote"]),500)

@monitoring.route("/stop_local")
def stop_local():
    return("",200)

@monitoring.route("/stop_remote",methods=['POST'])
def stop_remote():
    if not request.form["remote"]:
        return ("",400)
    gru.stop_monitoring_remote(request.form["remote"])
    return ("",200)

@monitoring.route("/add_regex_local",methods=['POST'])
def add_regex_local():
    if not request.form["regex"]:
        return ("",400)
    gru.add_regex_local(request.form["regex"])
    return ("", 200)

@monitoring.route("/add_regex_remote",methods=['POST'])
def add_regex_remote():
    if not request.form["remote"] or not request.form["regex"]:
        return ("",400)

    gru.add_regex_remote(request.form["remote"],request.form["regex"])
    return ("", 200)

@monitoring.route("/remove_regex_local",methods=['POST'])
def remove_regex_local():
    if not request.form["regex"]:
        return ("",400)

    gru.remove_regex_local(request.form["regex"])
    return ("", 200)

@monitoring.route("/remove_regex_remote",methods=['POST'])
def remove_regex_remote():
    if not request.form["remote"] or not request.form["regex"]:
        return ("",400)

    gru.remove_regex_remote(request.form["remote"], request.form["regex"])
    return ("", 200)


@monitoring.route("/list_regex_local")
def list_regex_local():
    return json.dumps(gru.list_regex_local())


@monitoring.route("/list_regex_remote",methods=['POST'])
def list_regex_remote():
    if not request.form["remote"]:
        return ("",400)

    return json.dumps(gru.list_regex_local(request.form["remote"]))


@monitoring.route("/get_events")
def get_events():
    return json.dumps(gru.get_events())



