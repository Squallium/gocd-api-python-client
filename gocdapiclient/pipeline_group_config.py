from gocdapiclient.endpoint import Endpoint
from gocdapiclient.pipeline import PipelineModel
from gocdapiclient.response import BaseModel, LinkModel


class PipelineGroupConfig(Endpoint):
    base_path = '/go/api/admin/pipeline_groups/'

    def __init__(self, server) -> None:
        super().__init__()

        self.server = server

        self._base_path = self.base_path

    def get_all(self):
        return self._get('', model_class=PipelineGroupsModel)

    def get(self, pipeline_group_name):
        return self._get(pipeline_group_name, model_class=PipelineGroupsModel)

    def create(self, body):
        return self._post(body=body, model_class=PipelineGroupModel)

class PipelineGroupsModel(BaseModel):

    def __init__(self, data) -> None:
        self._links: LinkModel = None
        self.groups: [PipelineGroupModel] = None

        super().__init__(data)

    @property
    def links(self):
        return self._links

    @property
    def _embedded(self):
        return None

    @_embedded.setter
    def _embedded(self, value):
        if len(value['groups']) > 0:
            self.groups = []
            for pipeline_group in value['groups']:
                self.groups.append(PipelineGroupModel(pipeline_group))


class PipelineGroupModel(BaseModel):

    def __init__(self, data) -> None:
        self._links: LinkModel = None
        self.name: str = None
        self.__pipelines: [PipelineModel] = None
        self.__authorization = {}

        super().__init__(data)

    @property
    def links(self):
        return self._links

    @property
    def pipelines(self):
        return self.__pipelines

    @pipelines.setter
    def pipelines(self, value):
        if len(value) > 0:
            self.__pipelines = []
            for pipeline in value:
                self.__pipelines.append(PipelineModel(pipeline))

    @property
    def authorization(self):
        return self.__authorization

    @authorization.setter
    def authorization(self, value):
        for key in value.keys():
            self.__authorization[key] = AuthorizationModel(value[key])


class AuthorizationModel(BaseModel):
    def __init__(self, data) -> None:
        self.users = []
        self.roles = []

        super().__init__(data)


class PipelineGroupConfigCreateModel:
    AUTH_VIEW = 'view'
    AUTH_OPERATE = 'operate'
    AUTH_ADMINS = 'admins'

    def __init__(self, pipeline_group_name) -> None:
        super().__init__()

        self.pipeline_group_name = pipeline_group_name
        self.users = {}
        self.roles = {}

    def add_auth_user(self, auth_level, user_name):
        if auth_level not in self.users.keys():
            self.users[auth_level] = []
        self.users.get(auth_level, []).append(user_name)

    def add_auth_role(self, auth_level, role_name):
        if auth_level not in self.roles.keys():
            self.roles[auth_level] = []
        self.roles.get(auth_level, []).append(role_name)

    def body(self):
        authorization = {}
        for key in self.users:
            if key not in authorization.keys():
                authorization[key] = {
                    'users': [],
                    'roles': []
                }
            authorization[key]['users'] = self.users[key]
        for key in self.roles:
            if key not in authorization.keys():
                authorization[key] = {
                    'users': [],
                    'roles': []
                }
            authorization[key]['roles'] = self.roles[key]

        return {
            'name': self.pipeline_group_name,
            'authorization': authorization
        }