# Copyright (c) 2018, The Johns Hopkins University/Applied Physics Laboratory
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

import pytest
import requests
import testtools


@pytest.mark.usefixtures("url")
class TestSLUGSAPI(testtools.TestCase):

    def setUp(self):
        super(TestSLUGSAPI, self).setUp()

    def test_request_root(self):
        """
        Test that a root-level request yields the right response..
        """
        response = requests.get(self.url + '/')

        self.assertEqual(response.status_code, 200)

        json = response.json()
        self.assertIsInstance(json, dict)
        self.assertEqual(len(json.keys()), 2)
        self.assertIn('users', json.keys())
        self.assertIn('groups', json.keys())

        users = json.get('users')
        groups = json.get('groups')
        self.assertIsInstance(users, list)
        self.assertIsInstance(groups, list)
        self.assertEqual(len(users), 2)
        self.assertEqual(len(groups), 3)
        self.assertIn('John', users)
        self.assertIn('Jane', users)
        self.assertIn('Human', groups)
        self.assertIn('Male', groups)
        self.assertIn('Female', groups)

    def test_request_users(self):
        """
        Test that a users request yields the right response..
        """
        response = requests.get(self.url + '/users')

        self.assertEqual(response.status_code, 200)

        json = response.json()
        self.assertIsInstance(json, dict)
        self.assertEqual(len(json.keys()), 1)
        self.assertIn('users', json.keys())

        users = json.get('users')
        self.assertIsInstance(users, list)
        self.assertEqual(len(users), 2)
        self.assertIn('John', users)
        self.assertIn('Jane', users)

    def test_request_groups(self):
        """
        Test that a groups request yields the right response..
        """
        response = requests.get(self.url + '/groups')

        self.assertEqual(response.status_code, 200)

        json = response.json()
        self.assertIsInstance(json, dict)
        self.assertEqual(len(json.keys()), 1)
        self.assertIn('groups', json.keys())

        groups = json.get('groups')
        self.assertIsInstance(groups, list)
        self.assertEqual(len(groups), 3)
        self.assertIn('Human', groups)
        self.assertIn('Male', groups)
        self.assertIn('Female', groups)

    def test_request_invalid_resource(self):
        """
        Test that a request for an invalid resource yields the right response.
        """
        response = requests.get(self.url + '/invalid')

        self.assertEqual(response.status_code, 404)

    def test_request_users_user(self):
        """
        Test that a users request for a specific user yields the right
        response.
        """
        response = requests.get(self.url + '/users/John')

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json())

    def test_request_users_user_invalid(self):
        """
        Test that a users request for an invalid user yields the right
        response.
        """
        response = requests.get(self.url + '/users/invalid')

        self.assertEqual(response.status_code, 404)

    def test_request_groups_group(self):
        """
        Test that a groups request for a specific group yields the right
        response.
        """
        response = requests.get(self.url + '/groups/Human')

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json())

    def test_request_groups_group_invalid(self):
        """
        Test that a groups request for an invalid group yields the right
        response.
        """
        response = requests.get(self.url + '/groups/invalid')

        self.assertEqual(response.status_code, 404)

    def test_request_users_user_groups(self):
        """
        Test that a groups request for a specific user yields the right result.
        """
        response = requests.get(self.url + '/users/John/groups')

        self.assertEqual(response.status_code, 200)

        json = response.json()
        self.assertIsInstance(json, dict)
        self.assertEqual(len(json.keys()), 1)
        self.assertIn('groups', json.keys())

        groups = json.get('groups')
        self.assertIsInstance(groups, list)
        self.assertEqual(len(groups), 2)
        self.assertIn('Human', groups)
        self.assertIn('Male', groups)

    def test_request_users_user_invalid_resource(self):
        """
        Test that a users request for an invalid user resource yields the
        right result.
        """
        response = requests.get(self.url + '/users/John/invalid')

        self.assertEqual(response.status_code, 404)

    def test_request_groups_group_users(self):
        """
        Test that a users request for a specific group yields the right result.
        """
        response = requests.get(self.url + '/groups/Human/users')

        self.assertEqual(response.status_code, 200)

        json = response.json()
        self.assertIsInstance(json, dict)
        self.assertEqual(len(json.keys()), 1)
        self.assertIn('users', json.keys())

        users = json.get('users')
        self.assertIsInstance(users, list)
        self.assertEqual(len(users), 2)
        self.assertIn('John', users)
        self.assertIn('Jane', users)

    def test_request_groups_group_invalid_resource(self):
        """
        Test that a groups request for an invalid group resource yields the
        right result.
        """
        response = requests.get(self.url + '/groups/Human/invalid')

        self.assertEqual(response.status_code, 404)

    def test_request_users_user_groups_group(self):
        """
        Test that a groups request for a specific group for a specific user
        yields the right result.
        """
        response = requests.get(self.url + '/users/John/groups/Human')

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json())

    def test_request_users_user_groups_group_invalid(self):
        """
        Test that a groups request for an invalid group for a specific user
        yields the right result.
        """
        response = requests.get(self.url + '/users/John/groups/invalid')

        self.assertEqual(response.status_code, 404)

    def test_request_groups_group_users_user(self):
        """
        Test that a users request for a specific user for a specific group
        yields the right result.
        """
        response = requests.get(self.url + '/groups/Female/users/Jane')

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json())

    def test_request_groups_group_users_user_invalid(self):
        """
        Test that a users request for an invalid user for a specific group
        yields the right result.
        """
        response = requests.get(self.url + '/groups/Female/users/invalid')

        self.assertEqual(response.status_code, 404)
