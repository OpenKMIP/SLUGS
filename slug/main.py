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

import cherrypy

from slug import controllers
from slug import plugins


if __name__ == '__main__':
    # Overall setup pattern taken from:
    # http://docs.cherrypy.org/en/latest/config.html

    # Set up global site configuration
    cherrypy.config.update({
        'log.access_file': '/var/log/slug/access.log',
        'log.error_file': '/var/log/slug/error.log'
    })

    # NOTE: Comment this out, or set request.show_tracebacks to True, to see
    # tracebacks with HTTP error results. Useful for development.
    cherrypy.config.update({
        'request.show_tracebacks': False
    })

    controller = controllers.MainController()
    plugins.FileMonitoringPlugin(
        cherrypy.engine,
        "/etc/slug/data.csv",
        controller.update
    ).subscribe()

    # Mount the app and pass it its own configuration
    cherrypy.tree.mount(controller, "/slug", {})

    if hasattr(cherrypy.engine, 'block'):
        # CherryPy 3.1 syntax
        cherrypy.engine.start()
        cherrypy.engine.block()
    else:
        # CherryPy 3.0 syntax
        cherrypy.server.quickstart()
        cherrypy.engine.start()
