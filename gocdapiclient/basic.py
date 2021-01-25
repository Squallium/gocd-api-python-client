from gocdapiclient.endpoint import Endpoint
from gocdapiclient.response import BaseModel


class Basic(Endpoint):
    base_path = 'go/api/'

    def __init__(self, server) -> None:
        """ A wrapper for the "Go API"

           Get version = '/go/api/version'
           Get current user = '/go/api/current_user'
           """
        super().__init__()

        self.server = server

    def version(self):
        response = self._get('version', model_class=VersionModel)

        # we store the server version for other request in the same server
        if response.is_ok and not self.server.version:
            self.server.version = response.payload.version

        return response

    def current_user(self):
        return self._get('current_user')

    def server_version(self):
        if not self.server.version:
            self.version()
        return self.server.version


class VersionModel(BaseModel):

    def __init__(self, data) -> None:
        self.version: str = None

        super().__init__(data)
