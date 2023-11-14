import json
from http import HTTPMethod
from http import HTTPStatus
from http.client import HTTPConnection

import src.log as log


class Client:
    def __init__(self, host, port):
        self._conn = HTTPConnection(host, port)
        self._auth_token = None


    def __del__(self):
        self._conn.close()


    def _request(self, method, url, body=None):
        headers = {
            'Accept': '*/*',
        }

        if self._auth_token:
            headers['Authorization'] = f'Bearer {self._auth_token}'

        if body:
            headers['Content-Type'] = 'application/json'

        self._conn.request(method, url, body, headers)
        response = self._conn.getresponse()
        responseBody = json.loads(response.read())

        try:
            error_message = ''
            if response.status != HTTPStatus.OK:
                error_message = f': {responseBody["error"]["message"]}'
                raise Exception(f'{response.status} {response.reason}')
        finally:
            log.info(
                f"{method} {self._conn.host}:{self._conn.port}{url}: "
                f"{response.status} {response.reason}{error_message}"
            )

        return responseBody['response']


    def login(self, username, password):
        body = json.dumps({
            'username': username,
            'password': password,
        })

        responseBody = self._request(HTTPMethod.POST, '/api/login_check', body)
        self._auth_token = responseBody['token']


    def create_group(self, name, description):
        body = json.dumps({
            'name': name,
            'description': description,
        })

        responseBody = self._request(HTTPMethod.POST, '/api/v1/media_group', body)

        return responseBody['id']


    def create_player(self, name, description, mac):
        body = json.dumps({
            'name': name,
            'description': description,
            'mac': mac,
        })

        responseBody = self._request(HTTPMethod.POST, '/api/v1/media_player', body)

        return responseBody['id']


    def add_player_to_group(self, player_id, group_id):
        body = json.dumps({
            'mediaGroup': group_id,
        })

        self._request(HTTPMethod.PATCH, f'/api/v1/media_player?id={player_id}', body)


    def delete_player(self, player_id):
        self._request(HTTPMethod.DELETE, f'/api/v1/media_player?id={player_id}')


    def delete_group(self, group_id):
        self._request(HTTPMethod.DELETE, f'/api/v1/media_group?id={group_id}')
