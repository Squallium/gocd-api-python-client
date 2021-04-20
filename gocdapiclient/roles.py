from gocdapiclient.endpoint import Endpoint
from gocdapiclient.response import EmbeddedModel, BaseModel, LinkModel
from gocdapiclient.server import Server


class Roles(Endpoint):
    base_path = '/go/api/admin/security/roles'

    def __init__(self, server) -> None:
        super().__init__()

        self.server = server

    def get_all(self):
        return self._get('', api_version=Server.VERSION_V3, model_class=RolesModel)

    def get(self, role_name):
        return self._get(role_name, api_version=Server.VERSION_V3, model_class=RoleModel)

    def create(self, body):
        return self._post(api_version=Server.VERSION_V3, body=body, model_class=RoleModel)


class RolesModel(EmbeddedModel):

    def __init__(self, data) -> None:
        super().__init__(data, 'roles', RoleModel)

    @property
    def roles(self):
        return self._values


class RoleModel(BaseModel):

    def __init__(self, data) -> None:
        self._links: LinkModel = None
        self.name: str = None

        self.__attributes = None
        self.__users = []

        super().__init__(data)

    @property
    def links(self):
        return self._links

    @property
    def users(self):
        return self.__users

    @property
    def attributes(self):
        return self.__attributes

    @attributes.setter
    def attributes(self, value):
        self.__attributes = value
        if 'users' in value:
            self.__users = value['users']


class RoleCreateModel:
    PERMISSION_ALLOW = 'allow'
    PERMISSION_DENY = 'deny'

    ACTION_VIEW = 'view'
    ACTION_ADMINISTER = 'administer'

    TYPE_ALL = '*'
    TYPE_ENVIRONMENT = 'environment'
    TYPE_CONFIG_REPOSITORY = 'config_repository'
    TYPE_CLUSTER_PROFILE = 'cluster_profile'
    TYPE_ELASTIC_AGENT_PROFILE = 'elastic_agent_profile'

    def __init__(self, role_name) -> None:
        super().__init__()

        self.role_name = role_name
        self.users = []
        self.policies = []

    def add_user(self, username):
        self.users.append(username)

    def add_policy(self, permission, action, policy_type, resource):
        self.policies.append({
            'permission': permission,
            'action': action,
            'type': policy_type,
            'resource': resource
        })

    def body(self):
        return {
            'name': self.role_name,
            'type': 'gocd',
            'attributes': {
                'users': self.users
            },
            'policy': self.policies
        }
