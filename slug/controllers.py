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


class MainController(object):
    def __init__(self):
        test_data = [
            ('Adam', 'Male'),
            ('Eve', 'Female'),
            ('Eve', 'Human'),
            ('Adam', 'Human')
        ]

        # NOTE: Use leading underscores here to prevent auto URL routing. Auto
        # routing prevents _cp_dispatch from being called.
        self._users = UsersController(test_data)
        self._groups = GroupsController(test_data)

    # NOTE: vpath is a required argument name here.
    def _cp_dispatch(self, vpath):
        length = len(vpath)
        controller = self

        # /collection
        if length >= 1:
            arg = vpath.pop(0)
            if arg == 'users':
                controller = self._users
            elif arg == 'groups':
                controller = self._groups
            else:
                raise cherrypy.HTTPError(404, "Resource not found.")

        # /collection/item
        if length >= 2:
            if controller == self._users:
                cherrypy.request.params['user'] = vpath.pop(0)
            else:
                cherrypy.request.params['group'] = vpath.pop(0)

        # /collection/item/sub-collection
        if length >= 3:
            arg = vpath.pop(0)
            if controller == self._users:
                if arg != 'groups':
                    # TODO (peter-hamilton) Craft more descriptive message.
                    raise cherrypy.HTTPError(404, "Resource not found.")
                else:
                    cherrypy.request.params['groups'] = True
            else:
                if arg != 'users':
                    # TODO (peter-hamilton) Craft more descriptive message.
                    raise cherrypy.HTTPError(404, "Resource not found.")
                else:
                    cherrypy.request.params['users'] = True

        # /collection/item/sub-collection/sub-item
        if length >= 4:
            if controller == self._users:
                cherrypy.request.params['group'] = vpath.pop(0)
            else:
                cherrypy.request.params['user'] = vpath.pop(0)

        # Invalid
        if length >= 5:
            # TODO (peter-hamilton) Craft more descriptive message.
            raise cherrypy.HTTPError(404, "Resource not found.")

        return controller

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        return {
            'users': self._users.list(),
            'groups': self._groups.list()
        }


class UsersController(object):

    def __init__(self, user_group_mapping=None):
        self.mapping = {}

        if user_group_mapping:
            for user_group in user_group_mapping:
                user_groups = self.mapping.get(user_group[0], [])
                user_groups.append(user_group[1])
                self.mapping.update([(user_group[0], user_groups)])

            # Do one final pass to remove duplicates.
            for user in self.mapping.keys():
                user_groups = self.mapping.get(user)
                self.mapping.update([(user, list(set(user_groups)))])

    def update(self, user_group_mapping=None):
        pass

    def list(self):
        return self.mapping.keys()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self, user=None, group=None, groups=False):
        if user:
            if user in self.mapping.keys():
                if groups:
                    user_groups = self.mapping.get(user)
                    if group:
                        if group in user_groups:
                            # TODO (peter-hamilton) Return 200 here.
                            return
                        else:
                            raise cherrypy.HTTPError(404, "Group not found.")
                    else:
                        return {'groups': user_groups}
                else:
                    # TODO (peter-hamilton) Return 200 here.
                    return
            else:
                raise cherrypy.HTTPError(404, "User not found.")
        else:
            return {'users': self.mapping.keys()}


class GroupsController(object):

    def __init__(self, user_group_mapping=None):
        self.mapping = {}

        if user_group_mapping:
            for user_group in user_group_mapping:
                user_groups = self.mapping.get(user_group[1], [])
                user_groups.append(user_group[0])
                self.mapping.update([(user_group[1], user_groups)])

            # Do one final pass to remove duplicates.
            for group in self.mapping.keys():
                group_users = self.mapping.get(group)
                self.mapping.update([(group, list(set(group_users)))])

    def update(self, user_group_mapping=None):
        pass

    def list(self):
        return self.mapping.keys()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self, group=None, user=None, users=False):
        if group:
            if group in self.mapping.keys():
                if users:
                    group_users = self.mapping.get(group)
                    if user:
                        if user in group_users:
                            # TODO (peter-hamilton) Return 200 here.
                            return
                        else:
                            raise cherrypy.HTTPError(404, "User not found.")
                    else:
                        return {'users': group_users}
                else:
                    # TODO (peter-hamilton) Return 200 here.
                    return
            else:
                raise cherrypy.HTTPError(404, "Group not found.")
        else:
            return {'groups': self.mapping.keys()}


if __name__ == '__main__':
    cherrypy.config.update({
        'log.access_file': '/var/log/slug/access.log',
        'log.error_file': '/var/log/slug/error.log'
    })

    # NOTE: Comment this out, or set request.show_tracebacks to True, to see
    # tracebacks with HTTP error results. Useful for development.
    cherrypy.config.update({
        'request.show_tracebacks': False
    })

    cherrypy.quickstart(MainController(), '/slug')

# Taken from http://docs.cherrypy.org/en/latest/config.html
#
# # Global site configuration
# cherrypy.config.update({...})
#
# # Mount each app and pass it its own configuration
# cherrypy.tree.mount(root1, "", appconf1)
# cherrypy.tree.mount(root2, "/forum", appconf2)
# cherrypy.tree.mount(root3, "/blog", appconf3)
#
# if hasattr(cherrypy.engine, 'block'):
#    # 3.1 syntax
#    cherrypy.engine.start()
#    cherrypy.engine.block()
# else:
#    # 3.0 syntax
#    cherrypy.server.quickstart()
#    cherrypy.engine.start()
