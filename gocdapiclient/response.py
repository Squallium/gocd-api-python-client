import re
import urllib
from urllib.parse import parse_qs

from requests import Response


class Response:

    def __init__(self, status_code, body, headers=None, ok_status=200, model_class=None):
        self.status_code = status_code
        self._body = body
        self.content_type = headers.get('content-type', '').split(';')[0] or False
        self.headers = headers or {}
        self.ok_status = ok_status or 200
        self.model_class = model_class

    @property
    def is_ok(self):
        """Whether this response is considered successful

        Returns
          bool: True if `status_code` is `ok_status`
        """
        return self.status_code == self.ok_status

    @property
    def is_json(self):
        """
        Returns:
          bool: True if `content_type` is `application/json`
        """
        return self.content_type and ((self.content_type.startswith('application/json') or
                                       re.match(r'application/vnd.go.cd.v(\d+)\+json', self.content_type)))

    @property
    def e_tag(self):
        return self.headers.get('ETag', None)

    @property
    def payload(self):
        result = None
        if self._body is not None:  # TODO stranger thing ever happen to me
            if self.content_type:
                if self.is_json:
                    if self.is_ok:
                        result = self.model_class(self._body.json()) if self.model_class else self._body.json()
                    else:
                        result = self._body.json()
                else:
                    result = self._body.text
            else:
                # TODO waiting for this to crash...
                result = self.model_class(self._body.json()) if self.model_class else self._body.json()

        return result

    @classmethod
    def from_request(cls, response, ok_status=None, model_class=None):
        return Response(
            response.status_code,
            response,
            response.headers,
            ok_status=ok_status,
            model_class=model_class
        )


class BaseModel:

    def __init__(self, data) -> None:
        super().__init__()

        # TODO maybe it will be unnecessary in the future
        self.data = data

        for k, v in data.items():
            if hasattr(self, k):
                setattr(self, k, v)


class LinkModel(BaseModel):

    def __init__(self, data) -> None:
        self.self: HRefModel = None
        self.doc: HRefModel = None
        self.find: HRefModel = None
        self.__next: HRefModel = None
        self.previous: HRefModel = None

        super().__init__(data)

    @property
    def next(self):
        return self.__next

    @next.setter
    def next(self, value):
        if value:
            self.__next = HRefModel(value)


class HRefModel(BaseModel):
    def __init__(self, data) -> None:
        self.href: str = None

        super().__init__(data)

    @property
    def after(self):
        result = None
        if self.href:
            parsed = urllib.parse.urlparse(self.href)
            result = parse_qs(parsed.query)['after']
        return result


class EmbeddedModel(BaseModel):
    def __init__(self, data, values_key, values_model) -> None:
        self._links: LinkModel = None

        self.__values_key = values_key
        self.__values_model = values_model
        self._values = []

        super().__init__(data)

    @property
    def links(self):
        return self._links

    @property
    def _embedded(self):
        return None

    @_embedded.setter
    def _embedded(self, value):
        if len(value[self.__values_key]) > 0:
            self._values = []
            for pipeline_group in value[self.__values_key]:
                self._values.append(self.__values_model(pipeline_group))
