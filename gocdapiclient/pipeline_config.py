from gocdapiclient.endpoint import Endpoint
from gocdapiclient.server import Server


class PipelineConfig(Endpoint):
    base_path = '/go/api/admin/pipelines/{pipeline_name}/'

    def __init__(self, server, pipeline_name) -> None:
        super().__init__()

        self.server = server
        self.pipeline_name = pipeline_name

        self._base_path = self.base_path.format(
            pipeline_name=pipeline_name
        )

    def delete(self):
        return self._delete(api_version=Server.VERSION_V11)
