from gocdapiclient.endpoint import Endpoint
from gocdapiclient.response import BaseModel


class Pipeline(Endpoint):
    base_path = '/go/api/pipelines/{pipeline_name}/'

    def __init__(self, server, pipeline_name) -> None:
        super().__init__()

        self.server = server
        self.pipeline_name = pipeline_name

        self._base_path = self.base_path.format(
            pipeline_name=pipeline_name
        )

    def status(self):
        """
            A wrapper for the "Go Pipeline API"
            status -> GET /go/api/pipelines/:pipeline_name/status
        """
        return self._get('status', api_version=None, model_class=PipelineStatusModel)

    def pause(self, pause_cause=None):
        body = {}
        headers = {}

        if not pause_cause:
            body.update({
                'pause_cause': pause_cause
            })

        # if not body we should add this to the header
        if not body:
            headers.update({
                'X-GoCD-Confirm': 'true'
            })
        return self._post('pause', body=body, headers=headers)

    def schedule(self, update_materials=None, env_vars=[], materials=[]):
        """
        Body
        {
         "environment_variables": [
           {
             "name": "USERNAME",
             "secure": false,
             "value": "bob"
           }
         ],
         "materials": [
           {
             "fingerprint": "b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b878ae4944c",
             "revision": "123"
           }
         ],
         "update_materials_before_scheduling": true
       }

        If no body you mas set the following header
        Missing required header 'X-GoCD-Confirm' with value 'true'
        :return:
        """
        body = {}
        headers = {}

        if update_materials is not None:
            body.update({
                'update_materials_before_scheduling': update_materials
            })
        if env_vars:
            body.update({
                'environment_variables': env_vars
            })
        if materials:
            body.update({
                'materials': materials
            })

        # if not body we should add this to the header
        if not body:
            headers.update({
                'X-GoCD-Confirm': 'true'
            })

        return self._post('schedule', body=body, headers=headers)

    def history(self, page_size=None, after=None, before=None):
        return self._get('history', model_class=PipelineHistoryModel)


class PipelineHistoryModel(BaseModel):

    def __init__(self, data) -> None:
        self.__pipelines: [PipelineModel] = None

        super().__init__(data)

    @property
    def pipelines(self):
        return self.__pipelines

    @pipelines.setter
    def pipelines(self, value):
        if len(value) > 0:
            self.__pipelines = []
            for pipeline in value:
                self.__pipelines.append(PipelineModel(pipeline))


class PipelineModel(BaseModel):

    def __init__(self, data) -> None:
        self.name: str = None
        self.counter: int = None
        self.__stages: [StageModel] = None

        super().__init__(data)

    @property
    def stages(self):
        return self.__stages

    @stages.setter
    def stages(self, value):
        if len(value) > 0:
            self.__stages = []
            for stage in value:
                self.__stages.append(StageModel(stage))


class StageModel(BaseModel):
    STATUS_BUILDING = 'Building'

    def __init__(self, data) -> None:
        self.result: str = None
        self.status: str = None
        self.name: str = None
        self.counter: str = None

        super().__init__(data)


class PipelineStatusModel(BaseModel):

    def __init__(self, data) -> None:
        self.pausedCause: str = None
        self.pausedBy: str = None
        self.paused: bool = None
        self.schedulable: bool = None
        self.locked: bool = None

        super().__init__(data)
