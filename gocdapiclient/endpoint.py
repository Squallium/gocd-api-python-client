import os

from gocdapiclient.server import Server


class Endpoint:
    base_path = None
    server: Server = None

    # for building parametric url paths
    _base_path = None

    def _get(self, path, api_version=Server.DEFAULT_VERSION, model_class=None):
        return self.server.request(Server.GET,
                                   os.path.join(self.__get_base_path, path),
                                   api_version=api_version,
                                   model_class=model_class)

    def _post(self, path, api_version=Server.DEFAULT_VERSION, body={}, headers={}, model_class=None):
        return self.server.request(Server.POST,
                                   os.path.join(self.__get_base_path, path),
                                   api_version=api_version,
                                   body=body,
                                   headers=headers,
                                   model_class=model_class)

    @property
    def __get_base_path(self):
        if getattr(self, 'base_path', None) is None:
            raise NotImplementedError('Base path is not set for this request')

        if not self._base_path:
            self._base_path = self.base_path

        return self._base_path
