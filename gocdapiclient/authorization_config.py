from gocdapiclient.endpoint import Endpoint
from gocdapiclient.response import BaseModel, LinkModel
from gocdapiclient.server import Server


class AuthorizationConfig(Endpoint):
    PLUGIN_ID_GOOGLE = 'cd.go.authorization.google'

    PLUGIN_KEY_CLIENT_ID = 'ClientId'
    PLUGIN_KEY_CLIENT_SECRET = 'ClientSecret'
    PLUGIN_KEY_ALLOWED_DOMAINS = 'AllowedDomains'

    base_path = '/go/api/admin/security/auth_configs'

    def __init__(self, server) -> None:
        super().__init__()

        self.server = server

        self._base_path = self.base_path

    def get_all(self):
        return self._get(api_version=Server.VERSION_V2, model_class=AuthorizationConfigsModel)

    def get(self, auth_config_id):
        return self._get(auth_config_id, api_version=Server.VERSION_V2)

    def create_google_authorization(self, auth_config_id, client_id, client_secret, allowed_domains):
        parameters = [{
            'key': 'ClientId',
            'value': client_id
        }, {
            'key': 'ClientSecret',
            'value': client_secret
        }, {
            'key': 'AllowedDomains',
            'value': allowed_domains
        }]

        return self.__create(auth_config_id, 'cd.go.authorization.google', parameters)

    def __create(self, auth_config_id, plugin_id, properties, allow_only_known_users_to_login=False):

        body = {
            'id': auth_config_id,
            'plugin_id': plugin_id,
            'allow_only_known_users_to_login': allow_only_known_users_to_login,
            'properties': properties
        }

        return self._post(api_version=Server.VERSION_V2, body=body, model_class=AuthorizationConfigModel)


class AuthorizationConfigsModel(BaseModel):

    def __init__(self, data) -> None:
        self._links: LinkModel = None
        self.auth_configs: [AuthorizationConfigModel] = None

        super().__init__(data)

    @property
    def links(self):
        return self._links

    @property
    def _embedded(self):
        return None

    @_embedded.setter
    def _embedded(self, value):
        if len(value['auth_configs']) > 0:
            self.auth_configs = []
            for pipeline_group in value['auth_configs']:
                self.auth_configs.append(AuthorizationConfigModel(pipeline_group))


class AuthorizationConfigModel(BaseModel):

    def __init__(self, data) -> None:
        self._links: LinkModel = None

        self.id: str = None

        super().__init__(data)

    @property
    def links(self):
        return self._links
