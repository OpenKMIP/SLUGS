# Copyright 2017, The Johns Hopkins University/Applied Physics Laboratory
# All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


from cherrypy.process import plugins

import os


class FileMonitoringPlugin(plugins.SimplePlugin):

    def __init__(self, bus, path):
        plugins.SimplePlugin.__init__(self, bus)

        self._path = None
        self._t = 0

        self.path = path

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        if os.path.exists(value):
            self._path = value
        else:
            raise ValueError("Path must be an existing file system path.")

    def start(self):
        self.bus.log('Starting data monitoring plugin...')
        self.bus.subscribe("main", self.check_path)

    def stop(self):
        self.bus.log('Stopping data monitoring plugin...')
        self.bus.unsubscribe("main", self.check_path)

    def check_path(self):
        t = os.path.getmtime(self.path)
        if t > self._t:
            self._t = t
            self.update_data()

    def update_data(self):
        self.bus.log("Monitored file updated, reloading data.")
