from gocdapiclient.endpoint import Endpoint
from gocdapiclient.response import BaseModel, LinkModel
from gocdapiclient.server import Server


class ConfigRepo(Endpoint):
    base_path = '/go/api/admin/config_repos'

    PLUGIN_ID_JSON = 'json.config.plugin'

    MATERIAL_GIT = 'git'

    PIPELINE_PATTERN = 'pipeline_pattern'
    ENVIRONMENT_PATTERN = 'environment_pattern'

    DIRECTIVE_ALLOW = 'allow'
    DIRECTIVE_DENY = 'deny'

    ACTION_REFER = 'refer'

    TYPE_ALL = '*'
    TYPE_PIPELINE = 'pipeline'
    TYPE_PIPELINE_GROUP = 'pipeline_group'
    TYPE_ENVIRONMENT = 'environment'

    def __init__(self, server) -> None:
        super().__init__()

        self.server = server

        self._base_path = self.base_path

    def get_all(self):
        return self._get(api_version=Server.VERSION_V4, model_class=ConfigReposModel)

    def get(self, config_repo_id):
        return self._get(config_repo_id, api_version=Server.VERSION_V4)

    def create(self, config_repo_id, plugin_id, material, configuration: [], rules: []):
        body = {
            'id': config_repo_id,
            'plugin_id': plugin_id,
            'material': material,
            'configuration': configuration,
            'rules': rules
        }

        return self._post(api_version=Server.VERSION_V4, body=body, model_class=ConfigRepoModel)

    @staticmethod
    def helper_create_rule(directive, action, rule_type, resource):
        """
        Return a rule for sending request

        :param directive:
        :param action:
        :param rule_type:
        :param resource:
        :return:
        """
        return {
            'directive': directive,
            'action': action,
            'type': rule_type,
            'resource': resource
        }

    @staticmethod
    def helper_create_configuration(key, pattern):
        """
        Return a configuration element

        :param key:
        :param pattern:
        :return:
        """
        return {
            'key': key,
            'value': pattern
        }

    @staticmethod
    def helper_create_material(material_type, at_url, at_branch=None, at_username=None, at_password=None,
                               at_auto_update=True):
        """
        Returns a material parameter of create function

        :param material_type:
        :param at_url:
        :param at_username:
        :param at_password:
        :param at_branch:
        :param at_auto_update:
        :return:
        """
        attributes = {
            'url': at_url,
            'auto_update': at_auto_update
        }
        if at_branch:
            attributes['branch'] = at_branch
        if at_username:
            attributes['username'] = at_username
        if at_password:
            attributes['password'] = at_password

        return {
            'type': material_type,
            'attributes': attributes
        }


class ConfigReposModel(BaseModel):

    def __init__(self, data) -> None:
        self._links: LinkModel = None
        self.config_repos: [ConfigRepoModel] = None

        super().__init__(data)

    @property
    def links(self):
        return self._links

    @property
    def _embedded(self):
        return None

    @_embedded.setter
    def _embedded(self, value):
        if len(value['config_repos']) > 0:
            self.config_repos = []
            for config_repo in value['config_repos']:
                self.config_repos.append(ConfigRepoModel(config_repo))


class ConfigRepoModel(BaseModel):

    def __init__(self, data) -> None:
        self._links: LinkModel = None

        self.id: str = None

        super().__init__(data)

    @property
    def links(self):
        return self._links
