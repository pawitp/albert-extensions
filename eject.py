# -*- coding: utf-8 -*-

"""Eject removable storages"""

import os
import subprocess

from albertv0 import *

__iid__ = 'PythonInterface/v0.1'
__prettyname__ = 'Eject'
__version__ = '1.0'
__trigger__ = 'eject '
__author__ = 'Pawit Pornkitprasan'
__dependencies__ = []

icon_path = iconLookup('media-eject')
mount_dir = '/run/media/' + os.environ['USER']

def eject(name):
    try:
        subprocess.check_output(['gio', 'mount', '-u', mount_dir + '/' + name], stderr=subprocess.STDOUT)
        subprocess.run(['notify-send', 'Successfully ejected ' + name])
    except subprocess.CalledProcessError as e:
        error = e.output.decode('utf-8').strip()
        subprocess.run(['notify-send', '-u', 'critical', 'Failed to eject ' + name, error])
        pass

def handleQuery(query):
    try:
        if query.isTriggered:
            items = []
            for file in os.listdir(mount_dir):
                actions = [ FuncAction('Eject ' + file, lambda: eject(file)) ]
                items.append(Item(id=__prettyname__ + '_' + file,
                                  text=file,
                                  subtext='Eject ' + file,
                                  completion='eject ' + file,
                                  icon=icon_path,
                                  actions=actions))
            return items
    except Exception as e:
        critical(e)
        pass
