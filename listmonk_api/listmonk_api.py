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

        response = self._session.get(f'{self.url}/subscribers', headers=self.headers, verify=self.verify)

        if response.status_code == 403:
            raise UnauthorizedError
        elif response.status_code == 401:
            raise AuthError
        elif response.status_code == 404:
            raise ParameterError

    ####################################################################################################################
    #                                              Subscribers API                                                     #
    ####################################################################################################################
    @require_auth
    def get_subscribers(self, query=None, list_id=None, max_pages=0, per_page=100):
        data = None
        response = self._session.get(f'{self.url}/subscribers?per_page={per_page}&x-total-pages',
                                     headers=self.headers, verify=self.verify)
        total_pages = int(response.headers['X-Total-Pages'])
        response = []
        subscriber_filter = f'?per_page={per_page}'
        if query:
            try:
                data = json.dumps(query, indent=4)
            except ValueError:
                raise ParameterError
        if list_id:
            if not isinstance(list_id, int) and not isinstance(list_id, list):
                raise ParameterError
            if isinstance(list_id, list):
                for single_list_id in list_id:
                    subscriber_filter = f'{subscriber_filter}&list_id={single_list_id}'
            else:
                subscriber_filter = f'{subscriber_filter}&list_id={list_id}'
        if max_pages == 0 or max_pages > total_pages:
            max_pages = total_pages
        for page in range(0, max_pages):
            response_page = self._session.get(f'{self.url}/subscribers{subscriber_filter}&page={page}',
                                              headers=self.headers, data=data, verify=self.verify)
            response_page = json.loads(response_page.text.replace('"', '\"'))
            response = response + response_page
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_subscriber(self, subscriber_id=None):
        if subscriber_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/subscribers/{subscriber_id}',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_subscribers_from_list(self, list_id=None):
        if list_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/subscribers/lists/{list_id}',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def create_subscriber(self, email=None, name=None, status=None, lists=None, attributes=None,
                          preconfirm_subscriptions=True):
        if email is None or name is None or status is None:
            raise MissingParameterError
        if isinstance(email, str) and isinstance(name, str) and isinstance(status, str):
            data = {'email': email, 'name': name, 'status': status}
        else:
            raise ParameterError
        if lists and isinstance(lists, list):
            data['lists'] = lists
        if attributes and isinstance(attributes, dict):
            data['attribs'] = attributes
        if isinstance(preconfirm_subscriptions, bool):
            data['preconfirm_subscriptions'] = preconfirm_subscriptions
        try:
            data = json.dumps(data, indent=4)
        except ValueError:
            raise ParameterError
        response = self._session.post(f'{self.url}/subscribers',
                                      headers=self.headers, data=data, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    ####################################################################################################################
    #                                                  Lists API                                                       #
    ####################################################################################################################
    @require_auth
    def get_lists(self, query=None, order_by=None, order=None, max_pages=0, per_page=100):
        data = None
        response = self._session.get(f'{self.url}/lists?per_page={per_page}&x-total-pages',
                                     headers=self.headers, verify=self.verify)
        total_pages = int(response.headers['X-Total-Pages'])
        response = []
        list_filter = f'?per_page={per_page}'
        if query:
            try:
                data = json.dumps(query, indent=4)
            except ValueError:
                raise ParameterError
        if order_by and order_by in ['name', 'status', 'created_at', 'updated_at']:
            list_filter = f'{list_filter}&order_by={order_by}'
        if order and order.upper() in ['ASC', 'DESC']:
            list_filter = f'{list_filter}&order={order}'
        if max_pages == 0 or max_pages > total_pages:
            max_pages = total_pages
        for page in range(0, max_pages):
            response_page = self._session.get(f'{self.url}/lists{list_filter}&page={page}',
                                              headers=self.headers, data=data, verify=self.verify)
            response_page = json.loads(response_page.text.replace('"', '\"'))
            response = response + response_page
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_list(self, list_id=None):
        if list_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/lists/{list_id}', headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def create_list(self, name=None, visibility_type=None, optin=None, tags=None):
        if name is None or type is None or optin is None:
            raise MissingParameterError
        data = {}
        if name:
            if not isinstance(name, str):
                raise ParameterError
            else:
                data['name'] = name
        if visibility_type:
            if not isinstance(visibility_type, str) and optin not in ['private', 'public']:
                raise ParameterError
            else:
                data['type'] = visibility_type
        if optin:
            if not isinstance(optin, str) and optin not in ['single', 'double']:
                raise ParameterError
            else:
                data['optin'] = optin
        if tags:
            if not isinstance(tags, list):
                raise ParameterError
            else:
                data['tags'] = tags
        try:
            data = json.dumps(data, indent=4)
        except ValueError:
            raise ParameterError
        response = self._session.post(f'{self.url}/lists', data=data, headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def edit_list(self, list_id=None, name=None, visibility_type=None, optin=None, tags=None):
        if list_id is None:
            raise MissingParameterError
        data = {}
        if name:
            if not isinstance(name, str):
                raise ParameterError
            else:
                data['name'] = name
        if visibility_type:
            if not isinstance(visibility_type, str) and optin not in ['private', 'public']:
                raise ParameterError
            else:
                data['type'] = visibility_type
        if optin:
            if not isinstance(optin, str) and optin not in ['single', 'double']:
                raise ParameterError
            else:
                data['optin'] = optin
        if tags:
            if not isinstance(tags, list):
                raise ParameterError
            else:
                data['tags'] = tags
        try:
            data = json.dumps(data, indent=4)
        except ValueError:
            raise ParameterError
        response = self._session.put(f'{self.url}/lists/{list_id}', data=data, headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    ####################################################################################################################
    #                                                 Import API                                                       #
    ####################################################################################################################
    @require_auth
    def get_subscriber_import_status(self):
        response = self._session.get(f'{self.url}/import/subscribers', headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_subscriber_import_logs(self):
        response = self._session.get(f'{self.url}/import/subscribers/logs', headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def import_subscribers(self, file=None, mode=None, delimiter=',', id_list=None, overwrite=True):
        if file is None or mode is None or id_list is None:
            raise MissingParameterError
        if not isinstance(id_list, list):
            raise ParameterError
        if mode not in ['subscribe', 'blocklist']:
            raise ParameterError
        if not isinstance(delimiter, str):
            raise ParameterError
        if not isinstance(overwrite, bool):
            raise ParameterError
        data = {
            'file': file,
            'mode': mode,
            'delim': delimiter,
            'lists': id_list,
            'overwrite': overwrite
        }
        try:
            data = json.dumps(data, indent=4)
        except ValueError:
            raise ParameterError
        response = self._session.get(f'{self.url}/import/subscribers/', headers=self.headers, data=data,
                                     verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def delete_subscriber_import(self):
        response = self._session.delete(f'{self.url}/import/subscribers/logs', headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    ####################################################################################################################
    #                                                Campaigns API                                                     #
    ####################################################################################################################
    @require_auth
    def get_campaigns(self, query=None, order_by=None, order=None, max_pages=0, per_page=100):
        data = None
        response = self._session.get(f'{self.url}/campaigns?per_page={per_page}&x-total-pages',
                                     headers=self.headers, verify=self.verify)
        total_pages = int(response.headers['X-Total-Pages'])
        response = []
        campaign_filter = f'?per_page={per_page}'
        if query:
            try:
                data = json.dumps(query, indent=4)
            except ValueError:
                raise ParameterError
        if order_by and order_by in ['name', 'status', 'created_at', 'updated_at']:
            campaign_filter = f'{campaign_filter}&order_by={order_by}'
        if order and order.upper() in ['ASC', 'DESC']:
            campaign_filter = f'{campaign_filter}&order={order}'
        if max_pages == 0 or max_pages > total_pages:
            max_pages = total_pages
        for page in range(0, max_pages):
            response_page = self._session.get(f'{self.url}/campaigns{campaign_filter}&page={page}',
                                              headers=self.headers, data=data, verify=self.verify)
            response_page = json.loads(response_page.text.replace('"', '\"'))
            response = response + response_page
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_campaign(self, campaign_id=None):
        if campaign_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/campaigns/{campaign_id}', headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_campaign_preview(self, campaign_id=None):
        if campaign_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/campaigns/{campaign_id}/preview', headers=self.headers,
                                     verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_campaign_stats(self, campaign_id=None):
        if campaign_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/campaigns/{campaign_id}/running/stats?campaign_id={campaign_id}',
                                     headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def create_campaign(self, name=None, subject=None, lists=None, from_email=None, send_type=None, content_type=None,
                        body=None, altbody=None, send_at=None, messenger=None, template_id=None, tags=None):
        if name is None or subject is None or lists is None or send_type is None or content_type is None \
                or body is None:
            raise MissingParameterError
        data = {}
        if isinstance(name, str):
            data['name'] = name
        if isinstance(subject, str):
            data['subject'] = subject
        if isinstance(lists, list):
            data['lists'] = lists
        if isinstance(from_email, str):
            data['from_email'] = from_email
        if send_type in ['regular', 'optin']:
            data['send_type'] = send_type
        else:
            raise ParameterError
        if content_type in ['richtext', 'html', 'markdown', 'plain']:
            data['content_type'] = content_type
        else:
            raise ParameterError
        if isinstance(body, str):
            data['body'] = body
        if isinstance(altbody, str):
            data['altbody'] = altbody
        if isinstance(send_at, str):
            data['send_at'] = send_at
        if isinstance(messenger, str):
            data['messenger'] = messenger
        if isinstance(template_id, int):
            data['template_id'] = template_id
        if isinstance(tags, list):
            data['tags'] = tags
        try:
            data = json.dumps(data, indent=4)
        except ValueError or AttributeError:
            raise ParameterError
        response = self._session.post(f'{self.url}/campaigns', data=data, headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def set_campaign_status(self, campaign_id=None, status=None):
        if campaign_id is None or status is None:
            raise MissingParameterError
        if status and status in ['scheduled', 'running', 'paused', 'cancelled']:
            data = {
                'status': status
            }
            try:
                data = json.dumps(data, indent=4)
            except ValueError or AttributeError:
                raise ParameterError
        else:
            raise ParameterError
        response = self._session.put(f'{self.url}/campaigns/{campaign_id}/status', data=data, headers=self.headers,
                                     verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def delete_campaign(self, campaign_id=None):
        if campaign_id is None:
            raise MissingParameterError
        response = self._session.delete(f'{self.url}/campaigns/{campaign_id}', headers=self.headers,
                                      verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    ####################################################################################################################
    #                                                  Media API                                                       #
    ####################################################################################################################
    @require_auth
    def get_media(self, media_id=None):
        if media_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/media', headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def upload_media(self, file=None):
        if file is None:
            raise MissingParameterError
        data = {'file': file}
        response = self._session.post(f'{self.url}/media', data=data, headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def delete_media(self, media_id=None):
        if media_id is None:
            raise MissingParameterError
        response = self._session.delete(f'{self.url}/media/{media_id}', headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response
    ####################################################################################################################
    #                                               Templates API                                                      #
    ####################################################################################################################
    @require_auth
    def get_templates(self, max_pages=0, per_page=100):
        data = None
        response = self._session.get(f'{self.url}/templates?per_page={per_page}&x-total-pages',
                                     headers=self.headers, verify=self.verify)
        total_pages = int(response.headers['X-Total-Pages'])
        response = []
        campaign_filter = f'?per_page={per_page}'
        if max_pages == 0 or max_pages > total_pages:
            max_pages = total_pages
        for page in range(0, max_pages):
            response_page = self._session.get(f'{self.url}/templates{campaign_filter}&page={page}',
                                              headers=self.headers, data=data, verify=self.verify)
            response_page = json.loads(response_page.text.replace('"', '\"'))
            response = response + response_page
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_template(self, template_id=None):
        if template_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/templates/{template_id}', headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def get_template_preview(self, template_id=None):
        if template_id is None:
            raise MissingParameterError
        response = self._session.get(f'{self.url}/templates/{template_id}/preview', headers=self.headers,
                                     verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def set_default_template(self, template_id=None):
        if template_id is None:
            raise MissingParameterError
        response = self._session.put(f'{self.url}/templates/{template_id}/default', headers=self.headers,
                                     verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    @require_auth
    def delete_template(self, template_id=None):
        if template_id is None:
            raise MissingParameterError
        response = self._session.delete(f'{self.url}/templates/{template_id}', headers=self.headers,
                                     verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response

    ####################################################################################################################
    #                                           Transactional API                                                      #
    ####################################################################################################################
    @require_auth
    def transactional_message(self, template_id=None, subscriber_email=None, subscriber_id=None, additional_data=None,
                              headers=None, content_type=None):
        if template_id is None:
            raise MissingParameterError
        data = {
            'template_id': template_id
        }
        if subscriber_id:
            data['subscriber_id']: subscriber_id
        elif subscriber_email:
            data['subscriber_email']: subscriber_email
        if additional_data:
            data['data']: additional_data
        if headers:
            data['headers']: headers
        if content_type:
            if content_type in ['html', 'markdown', 'plain']:
                data['content_type']: content_type
            else:
                raise ParameterError
        response = self._session.post(f'{self.url}/tx', data=data, headers=self.headers, verify=self.verify)
        try:
            return response.json()
        except ValueError or AttributeError:
            return response
