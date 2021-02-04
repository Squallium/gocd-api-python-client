from gocdapiclient.endpoint import Endpoint
from gocdapiclient.pipeline import PipelineModel
from gocdapiclient.response import BaseModel, LinkModel


class PipelineInstance(Endpoint):
    base_path = '/go/api/pipelines/{pipeline_name}/'

    def __init__(self, server, pipeline_name) -> None:
        super().__init__()

        self.server = server
        self.pipeline_name = pipeline_name

        self._base_path = self.base_path.format(
            pipeline_name=pipeline_name
        )

    def history(self, page_size=None, after=None, before=None):
        params = {}
        if page_size:
            params['page_size'] = page_size
        if after:
            params['after'] = after
        if before:
            params['before'] = before

        return self._get('history', params=params, model_class=PipelineHistoryModel)


class PipelineHistoryModel(BaseModel):

    def __init__(self, data) -> None:
        self.__links: LinkModel = None
        self.__pipelines: [PipelineModel] = None

        super().__init__(data)

    @property
    def links(self):
        return self._links

    @property
    def _links(self):
        return self.__links

    @_links.setter
    def _links(self, value):
        self.__links = LinkModel(value)

    @property
    def pipelines(self):
        return self.__pipelines

    @pipelines.setter
    def pipelines(self, value):
        if len(value) > 0:
            self.__pipelines = []
            for pipeline in value:
                self.__pipelines.append(PipelineModel(pipeline))
