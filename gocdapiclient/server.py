import logging
import urllib
from urllib.parse import urljoin

import requests

from gocdapiclient.response import Response


class Server:
    # available api versions
    VERSION_V1 = 'v1'
    VERSION_V2 = 'v2'
    VERSION_V3 = 'v3'
    VERSION_V4 = 'v4'
    VERSION_V11 = 'v11'

    DEFAULT_VERSION = VERSION_V1

    GET = 'get'
    POST = 'post'
    PUT = 'put'
    DELETE = 'delete'
    PATCH = 'patch'

    def __init__(self, host=None, token=None, verify=None) -> None:
        super().__init__()

        self.host = host
        self.token = token
        self.verify = verify
        self.version = None
        self.default_headers = {
            'Authorization': f'bearer {self.token}'
        }

    def request(self, method, path, api_version, params=None, body={}, headers={}, model_class=None):
        # creating the header
        final_headers = self.default_headers.copy()
        final_headers.update(headers)
        if api_version:
            final_headers['Accept'] = f'application/vnd.go.cd.{api_version}+json'

        url = urljoin(self.host, path)
        logging.warning(f'{url}{"?" + urllib.parse.urlencode(params, doseq=True) if params else ""}')

        if method == self.GET:
            response = requests.get(url,
                                    params=params,
                                    verify=self.verify,
                                    headers=final_headers)
        elif method == self.POST:
            response = requests.post(url,
                                     json=body,
                                     verify=self.verify,
                                     headers=final_headers)
        elif method == self.PUT:
            response = requests.put(url,
                                    json=body,
                                    verify=self.verify,
                                    headers=final_headers)
        elif method == self.DELETE:
            response = requests.delete(url,
                                       verify=self.verify,
                                       headers=final_headers)
        elif method == self.PATCH:
            response = requests.patch(url,
                                      json=body,
                                      verify=self.verify,
                                      headers=final_headers)
        else:
            raise NotImplementedError(f'Request method {method} no implemented')

        return Response.from_request(response, model_class=model_class)
