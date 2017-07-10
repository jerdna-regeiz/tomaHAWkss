# -*- coding: utf-8 -*-
from monitoring import Monitoring
import json
from flask import request

from flask import Flask

app = Flask(__name__)
monitor = None


@app.route("/add_regex", methods=['POST'])
def add_regex():
    # TODO signalisieren wenn regex bereits vorhanden oder ungültig
    try:
        monitor.add_regex(request.form["regex"])
        return ("", 201)
    except:
        return ("",400)


@app.route("/del_regex", methods=['POST'])
def del_regex():
    print("removing regex: " + request.form["regex"])
    monitor.remove_regex(request.form["regex"])

    return ("",200)


@app.route("/list_regex")
def list_regex():
    return json.dumps(monitor.list_regex())

@app.route("/get_events")
def get_events():
    return json.dumps(monitor.get_events_dict())

@app.route("/stop")
def stop():
    monitor.stop()
    return ("",200)


def main():
    monitor = Monitoring()
    monitor.start()

    app.run(debug=True, use_reloader=False)

if __name__ == "__main__":
    main()
