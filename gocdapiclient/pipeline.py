from datetime import datetime

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


class MaterialAttrsModel(BaseModel):
    def __init__(self, data) -> None:
        self.url: str = None
        self.destination: str = None
        self.filter: str = None
        self.invert_filter: bool = None
        self.name: str = None
        self.auto_update: bool = None
        self.branch: str = None
        self.submodule_folder: str = None
        self.shallow_clone: bool = None

        super().__init__(data)


class MaterialModel(BaseModel):

    def __init__(self, data) -> None:
        self.type: str = None
        self.__attributes: [MaterialAttrsModel] = None

        super().__init__(data)

    @property
    def attributes(self):
        return self.__attributes

    @attributes.setter
    def attributes(self, value):
        self.__attributes = MaterialAttrsModel(value)


class PipelineModel(BaseModel):

    def __init__(self, data) -> None:
        self.name: str = None
        self.counter: int = None
        self.__scheduled_date: datetime = None
        self.__materials: [MaterialModel] = None
        self.__stages: [StageModel] = None

        super().__init__(data)

    @property
    def materials(self):
        return self.__materials

    @materials.setter
    def materials(self, value):
        if len(value) > 0:
            self.__materials = []
            for material in value:
                self.__materials.append(MaterialModel(material))

    @property
    def stages(self):
        return self.__stages

    @stages.setter
    def stages(self, value):
        if len(value) > 0:
            self.__stages = []
            for stage in value:
                self.__stages.append(StageModel(stage))

    @property
    def scheduled_date(self):
        return self.__scheduled_date

    @scheduled_date.setter
    def scheduled_date(self, value):
        self.__scheduled_date = datetime.fromtimestamp(value / 1000.0)


class StageModel(BaseModel):
    STATUS_BUILDING = 'Building'

    def __init__(self, data) -> None:
        self.result: str = None
        self.status: str = None
        self.name: str = None
        self.counter: str = None
        self.__jobs: [JobModel] = None

        super().__init__(data)

    @property
    def jobs(self):
        return self.__jobs

    @jobs.setter
    def jobs(self, value):
        if len(value) > 0:
            self.__jobs = []
            for job in value:
                self.__jobs.append(StageModel(job))


class JobModel(BaseModel):

    def __init__(self, data) -> None:
        self.name: str = None

        super().__init__(data)


class PipelineStatusModel(BaseModel):

    def __init__(self, data) -> None:
        self.pausedCause: str = None
        self.pausedBy: str = None
        self.paused: bool = None
        self.schedulable: bool = None
        self.locked: bool = None

        super().__init__(data)
