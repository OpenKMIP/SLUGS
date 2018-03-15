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

import cherrypy
import mock
import os
import shutil
import tempfile
import testtools

from slugs import plugins


class TestFileMonitoringPlugin(testtools.TestCase):

    def setUp(self):
        super(TestFileMonitoringPlugin, self).setUp()

        self.temp_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.temp_dir)

        self.temp_file = tempfile.NamedTemporaryFile(
            dir=self.temp_dir,
            delete=False
        )

    def test_init(self):
        """
        Test that a FileMonitoringPlugin can be built without error.
        """
        callback = mock.MagicMock()
        plugin = plugins.FileMonitoringPlugin(
            cherrypy.engine,
            self.temp_file.name,
            callback
        )

        self.assertEqual(plugin.bus, cherrypy.engine)
        self.assertEqual(plugin._path, self.temp_file.name)
        self.assertEqual(plugin._callback, callback)

    def test_path(self):
        """
        Test that the path attribute of a FileMonitoringPlugin can be set and
        accessed correctly.
        """
        callback = mock.MagicMock()
        plugin = plugins.FileMonitoringPlugin(
            cherrypy.engine,
            self.temp_file.name,
            callback
        )
        plugin.bus = mock.MagicMock(spec=cherrypy.engine)

        self.assertEqual(plugin.path, self.temp_file.name)

        temp_file = tempfile.NamedTemporaryFile(
            dir=self.temp_dir,
            delete=False
        )

        plugin.path = temp_file.name
        self.assertEqual(plugin.path, temp_file.name)

    def test_invalid_path(self):
        """
        Test that the right error is raised when setting an invalid path on a
        FileMonitoringPlugin.
        """
        callback = mock.MagicMock()
        plugin = plugins.FileMonitoringPlugin(
            cherrypy.engine,
            self.temp_file.name,
            callback
        )
        plugin.bus = mock.MagicMock(spec=cherrypy.engine)

        args = [plugin, 'path', 'invalid']
        self.assertRaisesRegexp(
            ValueError,
            "Monitored file 'invalid' must be an existing file.",
            setattr,
            *args
        )

    def test_start(self):
        """
        Test that the FileMonitoringPlugin logs the right message and
        subscribes to the right bus channel when started.
        """
        callback = mock.MagicMock()
        plugin = plugins.FileMonitoringPlugin(
            cherrypy.engine,
            self.temp_file.name,
            callback
        )
        plugin.bus = mock.MagicMock(spec=cherrypy.engine)

        plugin.bus.log.assert_not_called()
        plugin.bus.subscribe.assert_not_called()

        plugin.start()

        plugin.bus.log.assert_called_once_with(
            "Starting file monitoring plugin for file: {}".format(plugin.path)
        )
        plugin.bus.subscribe.assert_called_once_with(
            "main",
            plugin.check_path
        )

    def test_stop(self):
        """
        Test that the FileMonitoringPlugin logs the right message and
        unsubscribes to the right bus channel when stopped.
        """
        callback = mock.MagicMock()
        plugin = plugins.FileMonitoringPlugin(
            cherrypy.engine,
            self.temp_file.name,
            callback
        )
        plugin.bus = mock.MagicMock(spec=cherrypy.engine)

        plugin.bus.log.assert_not_called()
        plugin.bus.unsubscribe.assert_not_called()

        plugin.stop()

        plugin.bus.log.assert_called_once_with(
            "Stopping file monitoring plugin for file: {}".format(plugin.path)
        )
        plugin.bus.unsubscribe.assert_called_once_with(
            "main",
            plugin.check_path
        )

    def test_check_path_with_no_update(self):
        """
        Test that no action is taken by the FileMonitoringPlugin when the
        monitored file is checked with no updates.
        """
        callback = mock.MagicMock()
        plugin = plugins.FileMonitoringPlugin(
            cherrypy.engine,
            self.temp_file.name,
            callback
        )
        plugin.bus = mock.MagicMock(spec=cherrypy.engine)
        plugin.update_data = mock.MagicMock()

        t = os.path.getmtime(plugin.path)
        plugin._t = t

        plugin.update_data.assert_not_called()

        plugin.check_path()

        self.assertEqual(plugin._t, t)
        plugin.update_data.assert_not_called()

    def test_check_path_with_update(self):
        """
        Test that the right action is taken by the FileMonitoringPlugin when
        the monitored file is checked with updates.
        """
        callback = mock.MagicMock()
        plugin = plugins.FileMonitoringPlugin(
            cherrypy.engine,
            self.temp_file.name,
            callback
        )
        plugin.bus = mock.MagicMock(spec=cherrypy.engine)
        plugin.update_data = mock.MagicMock()

        self.assertEqual(plugin._t, 0)
        plugin.update_data.assert_not_called()

        plugin.check_path()

        self.assertNotEqual(plugin._t, 0)
        plugin.update_data.assert_called_once()

    def test_update_data_with_no_data(self):
        """
        Test that the FileMonitoringPlugin processes an empty data file
        correctly.
        """
        callback = mock.MagicMock()
        plugin = plugins.FileMonitoringPlugin(
            cherrypy.engine,
            self.temp_file.name,
            callback
        )
        plugin.bus = mock.MagicMock(spec=cherrypy.engine)

        plugin.bus.log.assert_not_called()
        callback.assert_not_called()

        plugin.update_data()

        plugin.bus.log.assert_called_once_with(
            "Monitored file ({}) updated. Reloading data.".format(plugin.path)
        )
        callback.assert_called_once_with([])

    def test_update_data_with_data(self):
        """
        Test that the FileMonitoringPlugin processes a data file correctly.
        """
        callback = mock.MagicMock()
        plugin = plugins.FileMonitoringPlugin(
            cherrypy.engine,
            self.temp_file.name,
            callback
        )
        plugin.bus = mock.MagicMock(spec=cherrypy.engine)

        plugin.bus.log.assert_not_called()
        callback.assert_not_called()

        with open(self.temp_file.name, 'w') as f:
            f.write("John,Male\n")
            f.write("Jane,Female\n")
            f.write("John,Human\n")
            f.write("Jane,Human\n")
            f.write("\n")
            f.write("# This is a comment.")

        plugin.update_data()

        plugin.bus.log.assert_called_once_with(
            "Monitored file ({}) updated. Reloading data.".format(plugin.path)
        )
        callback.assert_called_once_with(
            [
                ['John', 'Male'],
                ['Jane', 'Female'],
                ['John', 'Human'],
                ['Jane', 'Human']
            ]
        )

    def test_update_data_with_bad_data(self):
        """
        Test that the FileMonitoringPlugin processes a data file correctly,
        handling data errors as expected.
        """
        callback = mock.MagicMock()
        plugin = plugins.FileMonitoringPlugin(
            cherrypy.engine,
            self.temp_file.name,
            callback
        )
        plugin.bus = mock.MagicMock(spec=cherrypy.engine)

        plugin.bus.log.assert_not_called()
        callback.assert_not_called()

        with open(self.temp_file.name, 'w') as f:
            f.write("John,Male\n")
            f.write("JaneFemale\n")
            f.write("John,Human\n")
            f.write("Jane,Human\n")

        plugin.update_data()

        plugin.bus.log.assert_any_call(
            "Monitored file ({}) updated. Reloading data.".format(plugin.path)
        )
        plugin.bus.log.assert_any_call(
            "Error parsing monitored file ({}). Halting data reload.".format(
                plugin.path
            )
        )
        callback.assert_not_called()
