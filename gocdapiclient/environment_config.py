from gocdapiclient.endpoint import Endpoint
from gocdapiclient.pipeline import PipelineModel
from gocdapiclient.response import BaseModel, LinkModel
from gocdapiclient.server import Server


class EnvironmentConfig(Endpoint):
    base_path = '/go/api/admin/environments'

    def __init__(self, server) -> None:
        super().__init__()

        self.server = server
        # self.pipeline_name = environment_name
        #
        # self._base_path = self.base_path.format(
        #     environment_name=environment_name
        # )

    def get_all(self):
        return self._get('', api_version=Server.VERSION_V3, model_class=EnvironmentsModel)

    def get(self, environment_name):
        return self._get(environment_name, api_version=Server.VERSION_V3, model_class=EnvironmentModel)

    def patch(self, environment_name, body):
        return self._patch(environment_name, api_version=Server.VERSION_V3, body=body, model_class=EnvironmentModel)

    def create(self, body):
        return self._post(api_version=Server.VERSION_V3, body=body, model_class=EnvironmentModel)


class EnvironmentsModel(BaseModel):

    def __init__(self, data) -> None:
        self._links: LinkModel = None
        self.environments: [EnvironmentModel] = None

        super().__init__(data)

    @property
    def links(self):
        return self._links

    @property
    def _embedded(self):
        return None

    @_embedded.setter
    def _embedded(self, value):
        if len(value['environments']) > 0:
            self.environments = []
            for pipeline_group in value['environments']:
                self.environments.append(EnvironmentModel(pipeline_group))


class EnvironmentModel(BaseModel):

    def __init__(self, data) -> None:
        self._links: LinkModel = None
        self.name: str = None
        self.__pipelines: [PipelineModel] = None
        self.__environment_variables: [EnvironmentVariableModel] = None

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
    def environment_variables(self):
        return self.__environment_variables

    @environment_variables.setter
    def environment_variables(self, value):
        if len(value) > 0:
            self.__environment_variables = []
            for env_var in value:
                self.__environment_variables.append(EnvironmentVariableModel(env_var))


class EnvironmentVariableModel(BaseModel):
    def __init__(self, data) -> None:
        self.secure: bool = None
        self.name: str = None
        self.value: str = None
        self.encrypted_value: str = None

        super().__init__(data)


class EnvironmentPatchModel:
    ADD = 'add'
    REMOVE = 'remove'

    def __init__(self) -> None:
        super().__init__()

        self.pipelines = {}
        self.environment_variables = {}

    def add_pipeline(self, pipeline_name):
        self.__array_append(self.pipelines, self.ADD, pipeline_name)

    def remove_pipeline(self, pipeline_name):
        self.__array_append(self.pipelines, self.REMOVE, pipeline_name)

    def add_env_var(self, name, value, secure=False):
        self.__array_append(self.environment_variables, self.ADD, {
            'secure': secure,
            'name': name,
            'value': value
        })

    def remove_env_var(self, name):
        self.__array_append(self.environment_variables, self.REMOVE, name)

    def body(self):
        return {
            'pipelines': self.pipelines,
            'environment_variables': self.environment_variables
        }

    def __array_append(self, collection, key, value):
        if key not in collection:
            collection[key] = []
        collection[key].append(value)


class EnvironmentCreateModel:

    def __init__(self, environment_name) -> None:
        super().__init__()

        self.environment_name = environment_name
        self.pipelines = []
        self.environment_variables = []

    def add_pipeline(self, pipeline_name):
        self.pipelines.append({
            'name': pipeline_name
        })

    def add_env_var(self, name, value, secure=False):
        self.environment_variables.append({
            'name': name,
            'value': value,
            'secure': secure
        })

    def body(self):
        return {
            'name': self.environment_name,
            'pipelines': self.pipelines,
            'environment_variables': self.environment_variables
        }
