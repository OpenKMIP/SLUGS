import cherrypy


class SLUGController(object):
    def __init__(self):
        test_data = [
            ('Adam', 'Male'),
            ('Eve', 'Female')
        ]

        self.users = Users(test_data)
        self.groups = Groups(test_data)

    def _cp_dispatch(self, path):
        length = len(path)
        controller = self

        # /collection
        if length >= 1:
            arg = path.pop()
            if arg == 'users':
                controller = self.users
            elif arg == 'groups':
                controller = self.groups
            else:
                raise cherrypy.HTTPError(404, "Resource not found.")

        # /collection/item
        if length >= 2:
            if controller == self.users:
                cherrypy.request.params['user'] = path.pop(0)
            else:
                cherrypy.request.params['group'] = path.pop(0)

        # /collection/item/sub-collection
        if length >= 3:
            arg = path.pop(0)
            if controller == self.users:
                if arg != 'groups':
                    # TODO (peter-hamilton) Craft more descriptive message.
                    raise cherrypy.HTTPError(404, "Resource not found.")
            else:
                if arg != 'users':
                    # TODO (peter-hamilton) Craft more descriptive message.
                    raise cherrypy.HTTPError(404, "Resource not found.")

        # /collection/item/sub-collection/sub-item
        if length >= 4:
            if controller == self.users:
                cherrypy.request.params['group'] = path.pop(0)
            else:
                cherrypy.request.params['user'] = path.pop(0)

        # Invalid
        if length >= 5:
            # TODO (peter-hamilton) Craft more descriptive message.
            raise cherrypy.HTTPError(404, "Resource not found.")

        return controller

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        return {
            'users': self.users.list(),
            'groups': self.groups.list()
        }


class Users(object):

    def __init__(self, user_group_mapping=None):
        self.mapping = {}

        if user_group_mapping:
            for user_group in user_group_mapping:
                user_groups = list(self.mapping.get(user_group[0], []))

                self.mapping.update([(
                    user_group[0],
                    set(user_groups.append(user_group[1]))
                )])

    def update(self, user_group_mapping=None):
        pass

    def list(self):
        return self.mapping.keys()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self, user=None, group=None):
        if user:
            groups = self.mapping.get(user)
            if group:
                if groups is None:
                    raise cherrypy.HTTPError(404, "User not found.")

                if group in groups:
                    # TODO (peter-hamilton) Return 200 here.
                    return
                else:
                    raise cherrypy.HTTPError(404, "Group not found.")
            else:
                return {'groups': groups}

        else:
            return {'users': self.mapping.keys()}


class Groups(object):

    def __init__(self, user_group_mapping=None):
        self.mapping = {}

        if user_group_mapping:
            for user_group in user_group_mapping:
                user_groups = list(self.mapping.get(user_group[1], []))
                self.mapping.update([(
                    user_group[1],
                    set(user_groups.append(user_group[0]))
                )])

    def update(self, user_group_mapping=None):
        pass

    def list(self):
        return self.mapping.keys()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self, group=None, user=None):
        if group:
            users = self.mapping.get(group)
            if user:
                if users is None:
                    raise cherrypy.HTTPError(404, "Group not found.")

                if user in users:
                    # TODO (peter-hamilton) Return 200 here.
                    return
                else:
                    raise cherrypy.HTTPError(404, "User not found.")
            else:
                return {'users': users}

        else:
            return {'groups': self.mapping.keys()}


if __name__ == '__main__':
    cherrypy.quickstart(SLUGController())
