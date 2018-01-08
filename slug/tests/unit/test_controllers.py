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
import mock
import testtools

from slug import controllers


class TestMainController(testtools.TestCase):

    def setUp(self):
        super(TestMainController, self).setUp()

    def test_init(self):
        """
        Test that a MainController can be built without error.
        """
        controller = controllers.MainController()

        self.assertIsInstance(controller._users, controllers.UsersController)
        self.assertIsInstance(controller._groups, controllers.GroupsController)

    def test_update_with_none(self):
        """
        Test that a MainController can be updated with no data without error.
        """
        controller = controllers.MainController()

        controller._users = mock.MagicMock(spec=controllers.UsersController)
        controller._groups = mock.MagicMock(spec=controllers.GroupsController)

        controller.update()

        controller._users.update.assert_called_once_with(None)
        controller._groups.update.assert_called_once_with(None)

    def test_update_with_data(self):
        """
        Test that a MainController can be updated with data without error.
        """
        controller = controllers.MainController()

        controller._users = mock.MagicMock(spec=controllers.UsersController)
        controller._groups = mock.MagicMock(spec=controllers.GroupsController)

        controller.update('test')

        controller._users.update.assert_called_once_with('test')
        controller._groups.update.assert_called_once_with('test')

    def test_cp_dispatch_level_one(self):
        """
        Test that MainController dispatching routes a Level 1 query to the
        right object controller
        """
        controller = controllers.MainController()

        users_mock = mock.MagicMock(spec=controllers.UsersController)
        groups_mock = mock.MagicMock(spec=controllers.GroupsController)

        controller._users = users_mock
        controller._groups = groups_mock

        result = controller._cp_dispatch(['users'])
        self.assertEqual(result, users_mock)

        result = controller._cp_dispatch(['groups'])
        self.assertEqual(result, groups_mock)

        args = [['invalid']]
        self.assertRaisesRegexp(
            cherrypy.HTTPError,
            "Collection not found.",
            controller._cp_dispatch,
            *args
        )

    def test_cp_dispatch_level_two(self):
        """
        Test that MainController dispatching routes a Level 2 query to the
        right object controller with the right request parameters.
        """
        controller = controllers.MainController()

        users_mock = mock.MagicMock(spec=controllers.UsersController)
        groups_mock = mock.MagicMock(spec=controllers.GroupsController)

        controller._users = users_mock
        controller._groups = groups_mock

        result = controller._cp_dispatch(['users', 'Adam'])
        self.assertEqual(result, users_mock)
        self.assertEqual(cherrypy.request.params['user'], 'Adam')

        result = controller._cp_dispatch(['groups', 'Human'])
        self.assertEqual(result, groups_mock)
        self.assertEqual(cherrypy.request.params['group'], 'Human')

    def test_cp_dispatch_level_three(self):
        """
        Test that MainController dispatching routes a Level 3 query to the
        right object controller with the right request parameters.
        """
        controller = controllers.MainController()

        users_mock = mock.MagicMock(spec=controllers.UsersController)
        groups_mock = mock.MagicMock(spec=controllers.GroupsController)

        controller._users = users_mock
        controller._groups = groups_mock

        result = controller._cp_dispatch(['users', 'Adam', 'groups'])
        self.assertEqual(result, users_mock)
        self.assertEqual(cherrypy.request.params['user'], 'Adam')
        self.assertEqual(cherrypy.request.params['groups'], True)

        args = [['users', 'Adam', 'invalid']]
        self.assertRaisesRegexp(
            cherrypy.HTTPError,
            "User attribute not found.",
            controller._cp_dispatch,
            *args
        )

        result = controller._cp_dispatch(['groups', 'Human', 'users'])
        self.assertEqual(result, groups_mock)
        self.assertEqual(cherrypy.request.params['group'], 'Human')
        self.assertEqual(cherrypy.request.params['users'], True)

        args = [['groups', 'Human', 'invalid']]
        self.assertRaisesRegexp(
            cherrypy.HTTPError,
            "Group attribute not found.",
            controller._cp_dispatch,
            *args
        )

    def test_cp_dispatch_level_four(self):
        """
        Test that MainController dispatching routes a Level 4 query to the
        right object controller with the right request parameters.
        """
        controller = controllers.MainController()

        users_mock = mock.MagicMock(spec=controllers.UsersController)
        groups_mock = mock.MagicMock(spec=controllers.GroupsController)

        controller._users = users_mock
        controller._groups = groups_mock

        result = controller._cp_dispatch(['users', 'Adam', 'groups', 'Human'])
        self.assertEqual(result, users_mock)
        self.assertEqual(cherrypy.request.params['user'], 'Adam')
        self.assertEqual(cherrypy.request.params['groups'], True)
        self.assertEqual(cherrypy.request.params['group'], 'Human')

        result = controller._cp_dispatch(['groups', 'Human', 'users', 'Adam'])
        self.assertEqual(result, groups_mock)
        self.assertEqual(cherrypy.request.params['group'], 'Human')
        self.assertEqual(cherrypy.request.params['users'], True)
        self.assertEqual(cherrypy.request.params['user'], 'Adam')

    def test_cp_dispatch_invalid_query(self):
        """
        Test that MainController dispatching handles an invalid query
        correctly.
        """
        controller = controllers.MainController()

        users_mock = mock.MagicMock(spec=controllers.UsersController)
        groups_mock = mock.MagicMock(spec=controllers.GroupsController)

        controller._users = users_mock
        controller._groups = groups_mock

        args = [['groups', 'Human', 'users', 'Adam', 'invalid']]
        self.assertRaisesRegexp(
            cherrypy.HTTPError,
            "Resource not found.",
            controller._cp_dispatch,
            *args
        )

    def test_index(self):
        """
        Test that a MainController can process a general index query without
        error.
        """
        controller = controllers.MainController()

        controller._users = mock.MagicMock(spec=controllers.UsersController)
        controller._groups = mock.MagicMock(spec=controllers.GroupsController)
        controller._users.list.return_value = ['Adam', 'Eve']
        controller._groups.list.return_value = ['Male', 'Female', 'Human']

        results = controller.index()

        self.assertIsInstance(results, dict)
        self.assertEqual(2, len(results.keys()))
        self.assertIn('users', results.keys())
        self.assertIn('groups', results.keys())

        self.assertEqual(2, len(results.get('users')))
        self.assertIn('Adam', results.get('users'))
        self.assertIn('Eve', results.get('users'))

        self.assertEqual(3, len(results.get('groups')))
        self.assertIn('Male', results.get('groups'))
        self.assertIn('Female', results.get('groups'))
        self.assertIn('Human', results.get('groups'))


class TestUsersController(testtools.TestCase):

    def setUp(self):
        super(TestUsersController, self).setUp()

    def test_init(self):
        self.skip('')

    def test_update_with_none(self):
        self.skip('')

    def test_update_with_data(self):
        self.skip('')

    def test_list(self):
        self.skip('')

    def test_index_a_bunch(self):
        self.skip('')


class TestGroupsController(testtools.TestCase):

    def setUp(self):
        super(TestGroupsController, self).setUp()

    def test_init(self):
        self.skip('')

    def test_update_with_none(self):
        self.skip('')

    def test_update_with_data(self):
        self.skip('')

    def test_list(self):
        self.skip('')

    def test_index_a_bunch(self):
        self.skip('')
