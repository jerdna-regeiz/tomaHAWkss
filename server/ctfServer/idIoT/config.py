#!/usr/bin/env python
# -*- coding: utf-8 -*-

from idIoT.ui.blueprint import ui
from idIoT.bib.blueprint import bib
from idIoT.monitoring.blueprint import monitoring

blueprints = [
            ui,
            bib,
            monitoring
        ]
