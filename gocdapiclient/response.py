import re

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

        for k, v in data.items():
            if hasattr(self, k):
                setattr(self, k, v)
