# Copyright 2018, The Johns Hopkins University/Applied Physics Laboratory
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

import argparse
import cherrypy
import os

from slugs import controllers
from slugs import plugins


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        dest="config",
        type=str,
        default="/etc/slugs/slugs.conf",
        help="Configuration file path."
    )
    return parser


def check_arguments(args):
    if not os.path.exists(args.config):
        raise ValueError(
            "Configuration file path '{}' does not exist.".format(args.config)
        )


def main():
    parser = build_parser()
    args = parser.parse_args()
    check_arguments(args)

    # Overall setup pattern taken from:
    # http://docs.cherrypy.org/en/latest/config.html

    # Set up global site configuration
    cherrypy.config.update(args.config)
    controller = controllers.MainController()

    # Mount the app and pass it its own configuration
    application = cherrypy.tree.mount(
        controller,
        "/slugs",
        config=args.config
    )
    plugins.FileMonitoringPlugin(
        cherrypy.engine,
        application.config.get('data').get('user_group_mapping'),
        controller.update
    ).subscribe()

    if hasattr(cherrypy.engine, 'block'):
        # CherryPy 3.1 syntax
        cherrypy.engine.start()
        cherrypy.engine.block()
    else:
        # CherryPy 3.0 syntax
        cherrypy.server.quickstart()
        cherrypy.engine.start()


if __name__ == '__main__':
    main()
