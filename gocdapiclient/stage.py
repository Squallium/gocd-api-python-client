from gocdapiclient.endpoint import Endpoint
from gocdapiclient.server import Server


class Stage(Endpoint):
    base_path = '/go/api/stages/{pipeline_name}/{pipeline_counter}/{stage_name}/'

    def __init__(self, server, pipeline_name, pipeline_counter, stage_name) -> None:
        super().__init__()

        self.server = server
        self.pipeline_name = pipeline_name
        self.pipeline_counter = pipeline_counter
        self.stage_name = stage_name

        self._base_path = self.base_path.format(
            pipeline_name=pipeline_name,
            pipeline_counter=pipeline_counter,
            stage_name=stage_name
        )

    def cancel(self, stage_counter):
        if stage_counter:
            return self._post(f'{stage_counter}/cancel', api_version=Server.VERSION_V2)
        else:
            raise NotImplementedError('Stage counter needed')
