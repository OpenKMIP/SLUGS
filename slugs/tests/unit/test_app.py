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
import mock
import shutil
import tempfile
import testtools

from slugs import app
from slugs import controllers


class TestApplication(testtools.TestCase):

    def setUp(self):
        super(TestApplication, self).setUp()

        self.temp_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.temp_dir)

        self.temp_file = tempfile.NamedTemporaryFile(
            dir=self.temp_dir,
            delete=False
        )

    def test_build_parser(self):
        """
        Test that a SLUGS ArgumentParser can be built without error.
        """
        result = app.build_parser()
        self.assertIsInstance(result, argparse.ArgumentParser)

    def test_check_arguments(self):
        """
        Test that a valid set of arguments is checked correctly.
        """
        kwargs = {'config': self.temp_file.name}
        args = argparse.Namespace(**kwargs)
        app.check_arguments(args)

    def test_check_arguments_with_invalid_config(self):
        """
        Test that an invalid 'config' argument generates the right error.
        """
        kwargs = {'config': 'invalid'}
        args = argparse.Namespace(**kwargs)

        self.assertRaisesRegexp(
            ValueError,
            "Configuration file path 'invalid' does not exist.",
            app.check_arguments,
            args
        )

    @mock.patch('cherrypy.engine')
    @mock.patch('slugs.plugins.FileMonitoringPlugin')
    @mock.patch('cherrypy.tree')
    @mock.patch('slugs.controllers.MainController')
    @mock.patch('cherrypy.config')
    @mock.patch('slugs.app.build_parser')
    def test_main(self,
                  build_parser_mock,
                  cherrypy_config_mock,
                  main_controller_mock,
                  cherrypy_tree_mock,
                  plugin_mock,
                  cherrypy_engine_mock):
        """
        Test that the main function can be run without error.
        """
        # Set up all the mocks.
        parser_mock = mock.MagicMock(spec=argparse.ArgumentParser)
        kwargs = {'config': self.temp_file.name}
        namespace = argparse.Namespace(**kwargs)
        parser_mock.parse_args.return_value = namespace
        build_parser_mock.return_value = parser_mock

        main_controller = mock.MagicMock(
            spec=controllers.MainController
        )
        update_mock = mock.MagicMock()
        main_controller.update = update_mock
        main_controller_mock.return_value = main_controller

        monitor_mock = mock.MagicMock()
        plugin_mock.return_value = monitor_mock

        application = mock.MagicMock(spec=cherrypy._cptree.Application)
        cherrypy_tree_mock.return_value = application

        if not hasattr(cherrypy_engine_mock, 'block'):
            setattr(cherrypy_engine_mock, 'block', mock.MagicMock())

        # Run main() and verify that the right calls were made.
        app.main()

        cherrypy_config_mock.update.assert_called_once_with(
            self.temp_file.name
        )
        main_controller_mock.assert_called()
        cherrypy_tree_mock.mount.assert_called_once_with(
            main_controller,
            "/slugs",
            config=self.temp_file.name
        )
        plugin_mock.assert_called()
        monitor_mock.subscribe.assert_called()
        cherrypy_engine_mock.start.assert_called()
        cherrypy_engine_mock.block.assert_called()

    @mock.patch('cherrypy.server')
    @mock.patch('cherrypy.engine')
    @mock.patch('slugs.plugins.FileMonitoringPlugin')
    @mock.patch('cherrypy.tree')
    @mock.patch('slugs.controllers.MainController')
    @mock.patch('cherrypy.config')
    @mock.patch('slugs.app.build_parser')
    def test_main_legacy(self,
                         build_parser_mock,
                         cherrypy_config_mock,
                         main_controller_mock,
                         cherrypy_tree_mock,
                         plugin_mock,
                         cherrypy_engine_mock,
                         cherrypy_server_mock):
        """
        Test that the main function can be run without error, assuming a
        legacy version of CherryPy is being used.
        """
        # Set up all the mocks.
        parser_mock = mock.MagicMock(spec=argparse.ArgumentParser)
        kwargs = {'config': self.temp_file.name}
        namespace = argparse.Namespace(**kwargs)
        parser_mock.parse_args.return_value = namespace
        build_parser_mock.return_value = parser_mock

        main_controller = mock.MagicMock(
            spec=controllers.MainController
        )
        update_mock = mock.MagicMock()
        main_controller.update = update_mock
        main_controller_mock.return_value = main_controller

        monitor_mock = mock.MagicMock()
        plugin_mock.return_value = monitor_mock

        application = mock.MagicMock(spec=cherrypy._cptree.Application)
        cherrypy_tree_mock.return_value = application

        if hasattr(cherrypy_engine_mock, 'block'):
            delattr(cherrypy_engine_mock, 'block')

        # Run main() and verify that the right calls were made.
        app.main()

        cherrypy_config_mock.update.assert_called_once_with(
            self.temp_file.name
        )
        main_controller_mock.assert_called()
        cherrypy_tree_mock.mount.assert_called_once_with(
            main_controller,
            "/slugs",
            config=self.temp_file.name
        )
        plugin_mock.assert_called()
        monitor_mock.subscribe.assert_called()
        cherrypy_server_mock.quickstart.assert_called()
        cherrypy_engine_mock.start.assert_called()
