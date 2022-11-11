#!/usr/bin/python
# coding: utf-8

import json
import requests
import urllib3
from base64 import b64encode

try:
    from listmonk_api.decorators import require_auth
except ModuleNotFoundError:
    from decorators import require_auth
try:
    from listmonk_api.exceptions import (AuthError, UnauthorizedError, ParameterError, MissingParameterError)
except ModuleNotFoundError:
    from exceptions import (AuthError, UnauthorizedError, ParameterError, MissingParameterError)


class Api(object):

    def __init__(self, url=None, username=None, password=None, token=None, verify=True):
        if url is None:
            raise MissingParameterError

        self._session = requests.Session()
        self.url = url
        self.headers = None
        self.verify = verify

        if self.verify is False:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        if token:
            self.headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
        elif username and password:
            user_pass = f'{username}:{password}'.encode()
            user_pass_encoded = b64encode(user_pass).decode()
            self.headers = {
                'Authorization': f'Basic {user_pass_encoded}',
                'Content-Type': 'application/json'
            }
        else:
            raise MissingParameterError

        response = self._session.get(f'{self.url}/projects', headers=self.headers, verify=self.verify)

        if response.status_code == 403:
            raise UnauthorizedError
        elif response.status_code == 401:
            raise AuthError
        elif response.status_code == 404:
            raise ParameterError

    ####################################################################################################################
    #                                                 Branches API                                                     #
    ####################################################################################################################
    @require_auth
    def get_branches(self, project_id=None):
        if project_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/projects/{project_id}/repository/branches',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response
