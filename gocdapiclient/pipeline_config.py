import logging
from collections import OrderedDict

from gocdapiclient.endpoint import Endpoint
from gocdapiclient.pipeline import PipelineModel
from gocdapiclient.server import Server


class PipelineConfig(Endpoint):
    base_path = '/go/api/admin/pipelines/'

    def __init__(self, server) -> None:
        super().__init__()

        self.server = server

        self._base_path = self.base_path

    def create(self, body):
        return self._post(api_version=Server.VERSION_V11, body=body, model_class=PipelineModel)

    def get(self, pipeline_name):
        return self._get(pipeline_name, api_version=Server.VERSION_V11, model_class=PipelineModel)

    def update(self, pipeline_name, body, if_match=None):
        return self._put(pipeline_name, api_version=Server.VERSION_V11, body=body, model_class=PipelineModel,
                         if_match=if_match)

    def delete(self, pipeline_name):
        return self._delete(pipeline_name, api_version=Server.VERSION_V11)


class PipelineConfigHelper:

    def __init__(self, pipeline_group_name, pipeline_name) -> None:
        super().__init__()

        self.pipeline_group_name = pipeline_group_name
        self.pipeline_name = pipeline_name
        self.environment_variables = []
        self.materials = []
        self.stages = OrderedDict()
        self.jobs = OrderedDict()
        self.tasks = OrderedDict()

    def add_env_var(self, name, value, secure=False):
        self.__add_env_var(self.environment_variables, name, value, secure)

    def add_material(self, mat_type, url, destination, name, branch, ignore=None):
        material = {
            'type': mat_type,
            'attributes': {
                'url': url,
                'destination': destination,
                'filter': None,
                'invert_filter': False,
                'name': name,
                'auto_update': True,
                'branch': branch,
                'submodule_folder': None,
                'shallow_clone': True
            }
        }

        if ignore:
            material['attributes']['filter'] = {
                'ignore': ignore
            }

        self.materials.append(material)

    def add_stage(self, name):
        self.stages[name] = {
            'name': name,
            'fetch_materials': True,
            'clean_working_directory': True,
            'never_cleanup_artifacts': True,
            'approval': {
                'type': 'success',
                'authorization': {
                    'roles': [],
                    'users': []
                }
            },
            'environment_variables': [],
            'jobs': []
        }

    def add_job(self, stage_name, name, timeout):
        if stage_name in self.stages.keys():
            if stage_name not in self.jobs.keys():
                self.jobs[stage_name] = OrderedDict()

            self.jobs[stage_name][name] = {
                'name': name,
                'run_instance_count': None,
                'timeout': timeout,
                'environment_variables': [],
                'resources': [],
                'tasks': [],
                'tabs': [],
                'artifacts': [],
                'properties': None
            }
        else:
            logging.error(f'Stage {stage_name} not found')

    def add_job_env_var(self, stage_name, job_name, name, value, secure=False):
        if stage_name in self.stages.keys() and job_name in self.jobs.keys():
            self.__add_env_var(self.jobs[stage_name][job_name]['environment_variables'], name, value, secure)

    def add_job_task(self, stage_name, job_name, task, on_cancel=None):
        if on_cancel:
            task['on_cancel'] = on_cancel
        self.jobs[stage_name][job_name]['tasks'].append(task)

    @staticmethod
    def generate_task(task_type, command, arguments, working_directory=None):
        result = {
            'type': task_type,
            'attributes': {
                'run_if': ['passed'],
                'command': command,
                'arguments': arguments
            }
        }

        if working_directory:
            result['working_directory'] = working_directory

        return result

    def __add_env_var(self, env_vars, name, value, secure):
        env_vars.append({
            'name': name,
            'value': value,
            'secure': secure
        })

    def create_body(self):
        stages = []
        for stage in self.stages.values():
            stage['jobs'] = list(self.jobs[stage['name']].values())
            stages.append(stage)

        result = {
            'group': self.pipeline_group_name,
            'pipeline': {
                'label_template': '${COUNT}',
                'lock_behavior': 'unlockWhenFinished',
                'name': self.pipeline_name,
                'template': None,
                'environment_variables': self.environment_variables,
                'materials': self.materials,
                'stages': stages
            }
        }
        return result

    def update_body(self):
        result = self.create_body()

        result['pipeline']['group'] = result['group']

        return result['pipeline']
