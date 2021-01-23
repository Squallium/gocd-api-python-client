from gocdapiclient.endpoint import Endpoint


class Artifact(Endpoint):
    base_path = '/go/files/{pipeline_name}/{pipeline_counter}/{stage_name}/{stage_counter}/'

    def __init__(self, server, pipeline_name, pipeline_counter, stage_name, stage_counter) -> None:
        """ A wrapper for the "Go Artifacts API"

           all_artifact = '/go/files/:pipeline_name/:pipeline_counter/:stage_name/:stage_counter/:job_name.json'
           get_artifact = '/go/files/:pipeline_name/:pipeline_counter/:stage_name/:stage_counter/:job_name/*path_to_file'
           """
        super().__init__()

        self.server = server
        self.pipeline_name = pipeline_name
        self.pipeline_counter = pipeline_counter
        self.stage_name = stage_name
        self.stage_counter = stage_counter

        self._base_path = self.base_path.format(
            pipeline_name=pipeline_name,
            pipeline_counter=pipeline_counter,
            stage_name=stage_name,
            stage_counter=stage_counter
        )

    def list(self, job_name):
        return self._get(f'{job_name}.json')

    def get(self, job_name, path_to_file):
        return self._get(f'{job_name}/{path_to_file}')