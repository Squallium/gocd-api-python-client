from gocdapiclient.endpoint import Endpoint
from gocdapiclient.pipeline import PipelineModel
from gocdapiclient.response import BaseModel, LinkModel


class PipelineGroupConfig(Endpoint):
    base_path = '/go/api/admin/pipeline_groups/'

    def __init__(self, server) -> None:
        super().__init__()

        self.server = server

        self._base_path = self.base_path

    def all(self):
        return self._get('', model_class=PipelineGroupsModel)


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


