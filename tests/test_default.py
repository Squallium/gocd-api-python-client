import json
import logging
import os

from gocdapiclient.basic import Basic, VersionModel
from gocdapiclient.server import Server

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    server_url = os.environ.get('SERVER_URL', None)
    personal_access_toke = os.environ.get('PERSONAL_ACCESS_TOKEN', None)
    verification = os.environ.get('VERIFICATION', True)

    server = Server(server_url, personal_access_toke, verification)

    # TODO basic
    basic = Basic(server)
    # version
    server_version: VersionModel = basic.version().payload
    logging.info(server_version.version)
    # autenticacion
    logging.info(json.dumps(basic.current_user().payload, indent=4, sort_keys=True))

    # # TODO pipelines
    # pipeline = Pipeline(server, 'pipeline-name')
    #
    # # pipeline status
    # pipeline_status: PipelineStatusModel = pipeline.status().payload
    # logging.info(f'Paused pipeline-> {pipeline_status.paused}')
    #
    # # pipeline schedule
    # logging.info(pipeline.schedule().payload)
    #
    # # pipeline status
    # pipeline_status: PipelineStatusModel = pipeline.status().payload
    # logging.info(f'Paused pipeline -> {pipeline_status.paused}')
    #
    # # TODO artifacts
    # artifact = Artifact(server,
    #                     'pipeline-name',
    #                     'pipeline-counter',
    #                     'stage-name',
    #                     'stage-counter')
    #
    # # acceso a artefactos de una ejecución
    # artifacts = artifact.list('pipeline-name')
    # logging.info(json.dumps(artifacts.payload, indent=4, sort_keys=True))
    #
    # # descarga de un artefacto concreto
    # console_log = artifact.get('pipeline-name', 'cruise-output/console.log')
    # with open('temp/console.log', 'w') as f:
    #     f.writelines(console_log.payload)
