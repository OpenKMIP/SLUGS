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
import threading


def synchronize(f):
    def decorator(self, *args, **kwargs):
        with self._lock:
            return f(self, *args, **kwargs)

    return decorator


class MainController(object):
    def __init__(self):
        self._lock = threading.RLock()

        # NOTE: Use leading underscores here to prevent auto URL routing. Auto
        # routing prevents _cp_dispatch from being called.
        self._users = UsersController()
        self._groups = GroupsController()

    @synchronize
    def update(self, data=None):
        self._users.update(data)
        self._groups.update(data)

    # NOTE: vpath is a required argument name for _cp_dispatch.
    @synchronize
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
                raise cherrypy.HTTPError(404, "Collection not found.")

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
                    raise cherrypy.HTTPError(404, "User attribute not found.")
                else:
                    cherrypy.request.params['groups'] = True
            else:
                if arg != 'users':
                    raise cherrypy.HTTPError(404, "Group attribute not found.")
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
            raise cherrypy.HTTPError(404, "Resource not found.")

        return controller

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @synchronize
    def index(self):
        return {
            'users': self._users.list(),
            'groups': self._groups.list()
        }


class UsersController(object):

    def __init__(self, user_group_mapping=None):
        self.mapping = {}
        self.update(user_group_mapping)

    def update(self, user_group_mapping=None):
        mapping = {}

        if user_group_mapping:
            for user_group in user_group_mapping:
                user_groups = mapping.get(user_group[0], [])
                user_groups.append(user_group[1])
                mapping.update([(user_group[0], user_groups)])

            # Do one final pass to remove duplicates.
            for user in mapping.keys():
                user_groups = mapping.get(user)
                mapping.update([(user, list(set(user_groups)))])

        self.mapping = mapping

    def list(self):
        return list(self.mapping.keys())

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self, user=None, groups=False, group=None):
        if user is not None:
            if user in self.mapping.keys():
                if groups:
                    user_groups = self.mapping.get(user)
                    if group is not None:
                        if group in user_groups:
                            return
                        else:
                            raise cherrypy.HTTPError(404, "Group not found.")
                    else:
                        return {'groups': user_groups}
                else:
                    return
            else:
                raise cherrypy.HTTPError(404, "User not found.")
        else:
            return {'users': list(self.mapping.keys())}


class GroupsController(object):

    def __init__(self, user_group_mapping=None):
        self.mapping = {}
        self.update(user_group_mapping)

    def update(self, user_group_mapping=None):
        mapping = {}

        if user_group_mapping:
            for user_group in user_group_mapping:
                user_groups = mapping.get(user_group[1], [])
                user_groups.append(user_group[0])
                mapping.update([(user_group[1], user_groups)])

            # Do one final pass to remove duplicates.
            for group in mapping.keys():
                group_users = mapping.get(group)
                mapping.update([(group, list(set(group_users)))])

        self.mapping = mapping

    def list(self):
        return list(self.mapping.keys())

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self, group=None, users=False, user=None):
        if group:
            if group in self.mapping.keys():
                if users:
                    group_users = self.mapping.get(group)
                    if user:
                        if user in group_users:
                            return
                        else:
                            raise cherrypy.HTTPError(404, "User not found.")
                    else:
                        return {'users': group_users}
                else:
                    return
            else:
                raise cherrypy.HTTPError(404, "Group not found.")
        else:
            return {'groups': list(self.mapping.keys())}
