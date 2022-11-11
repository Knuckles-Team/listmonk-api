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
        
    @require_auth
    def get_campaigns(self):
        r = self._session.get(self.api_url + f"/campaigns?page=1&per_page=100", headers=self.headers, verify=False)
        return r.json()

    @require_auth
    def get_campaign(self, campaign_id=None):
        if campaign_id is None:
            raise MissingParameterError
        r = self._session.get(self.api_url + f"/campaigns/{campaign_id}", headers=self.headers, verify=False)
        return r.json()

    @require_auth
    def create_campaign(self, data=None, attempt=0):
        if data is None:
            raise MissingParameterError
        r = self._session.post(self.api_url + f"/campaigns", data=data, headers=self.headers, verify=False)
        try:
            return r.json()
        except (json.JSONDecodeError) as e:
            if attempt < 9:
                print(f"Unable to create campaign attempt {attempt}")
                self.create_campaign(data=data, attempt=attempt+1)
            else:
                print("Unable to create campaign after 9 attempts. Error: ", e)
                r = f"{e}"
                return r

    @require_auth
    def update_campaign(self, campaign_id=None, data=None):
        if campaign_id is None or data is None:
            raise MissingParameterError
        r = self._session.post(self.api_url + f"/campaigns/{campaign_id}", data=data, headers=self.headers, verify=False)
        return r.json()

    @require_auth
    def set_campaign_status(self, campaign_id=None, data=None,):
        if campaign_id is None or data is None:
            raise MissingParameterError
        r = self._session.put(self.api_url + f"/campaigns/{campaign_id}/status", data=data, headers=self.headers, verify=False)
        return r.json()

    @require_auth
    def get_lists(self):
        r = self._session.get(self.api_url + f"/lists?page=1&per_page=100", headers=self.headers, verify=False)
        return r.json()

    @require_auth
    def get_list(self, list_id=None):
        if list_id is None:
            raise MissingParameterError
        r = self._session.get(self.api_url + f"/lists/{list_id}", headers=self.headers, verify=False)
        return r.json()

    @require_auth
    def create_list(self, data=None):
        if data is None:
            raise MissingParameterError
        r = self._session.post(self.api_url + f"/lists", data=data, headers=self.headers, verify=False)
        return r.json()

    @require_auth
    def get_templates(self):
        r = self._session.get(self.api_url + f"/templates?page=1&per_page=100", headers=self.headers, verify=False)
        return r.json()

    @require_auth
    def get_template(self, template_id=None):
        if template_id is None:
            raise MissingParameterError
        r = self._session.get(self.api_url + f"/templates/{template_id}", headers=self.headers, verify=False)
        return r.json()

    @require_auth
    def set_default_template(self, data=None):
        if data is None:
            raise MissingParameterError
        r = self._session.post(self.api_url + f"/templates", data=data, headers=self.headers, verify=False)

