import os

from gocdapiclient.server import Server


class Endpoint:
    base_path = None
    server: Server = None

    # for building parametric url paths
    _base_path = None

    def _get(self, path=None, api_version=Server.DEFAULT_VERSION, params=None, model_class=None):
        return self.server.request(Server.GET,
                                   os.path.join(self.__get_base_path, path) if path else self.__get_base_path,
                                   api_version=api_version, params=params, model_class=model_class)

    def _post(self, path=None, api_version=Server.DEFAULT_VERSION, body={}, headers={}, model_class=None):
        return self.server.request(Server.POST,
                                   os.path.join(self.__get_base_path, path) if path else self.__get_base_path,
                                   api_version=api_version, body=body, headers=headers, model_class=model_class)

    def _put(self, path=None, api_version=Server.DEFAULT_VERSION, body={}, headers={}, if_match=None, model_class=None):
        if if_match:
            headers.update({
                'If-Match': if_match
            })
        return self.server.request(Server.PUT,
                                   os.path.join(self.__get_base_path, path) if path else self.__get_base_path,
                                   api_version=api_version, body=body, headers=headers, model_class=model_class)

    def _delete(self, path=None, api_version=Server.DEFAULT_VERSION, body={}, headers={}):
        # if not body we should add this to the header
        if not body:
            headers.update({
                'X-GoCD-Confirm': 'true'
            })

        return self.server.request(Server.DELETE,
                                   os.path.join(self.__get_base_path, path) if path else self.__get_base_path,
                                   api_version=api_version, body=body, headers=headers)

    def _patch(self, path=None, api_version=Server.DEFAULT_VERSION, body={}, headers={}, model_class=None):
        return self.server.request(Server.PATCH,
                                   os.path.join(self.__get_base_path, path) if path else self.__get_base_path,
                                   api_version=api_version, body=body, headers=headers, model_class=model_class)

    @property
    def __get_base_path(self):
        if getattr(self, 'base_path', None) is None:
            raise NotImplementedError('Base path is not set for this request')

        if not self._base_path:
            self._base_path = self.base_path

        return self._base_path
