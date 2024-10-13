from abc import ABC, abstractmethod

from requests import Session, Response

from logic.cfg import Config
from logic.models.api import TeamcityUser, EndpointName, Roles
from logic.utils import generate_faker_name


class TCConnector(ABC):
    def __init__(self, user: TeamcityUser | None = None):
        self._cfg = Config()
        self.session = Session()
        self.session.headers.update(
            {
                'Accept': 'application/json',
                'Cookie': '',
                'Content-Type': 'application/json'
            }
        )
        if user:
            self.session.auth = user.credentials

    @property
    def url(self) -> str:
        base = self._cfg.host if self.session.auth else self._cfg.host_with_token
        return f'{base}/httpAuth/app/rest/{self.endpoint_name}'

    @property
    @abstractmethod
    def endpoint_name(self) -> str:
        raise NotImplemented

    def delete(self, tail: str = '', **params):
        return self.session.delete(self.url + tail, params=params)

    def get(self, tail: str = '', **params):
        return self.session.get(self.url + tail, params=params)

    def post(self, payload: dict, tail: str = ''):
        return self.session.post(self.url + tail, json=payload)

    def put(self, payload: dict, tail: str = ''):
        return self.session.put(self.url + tail, data=payload)



class TCProjects(TCConnector):

    @property
    def endpoint_name(self) -> str:
        return EndpointName.projects

    def create(self, project_id: str) -> Response:
        payload = {
            'parentProject': {
                'locator': '_Root'
            },
            'name': generate_faker_name(),
            'id': project_id,
            'copyAllAssociatedSettings': True
        }
        return self.post(payload)

    def delete_project(self, project_id):
        return self.delete(tail=f'/id:{project_id}')


class TCBuildTypes(TCConnector):

    @property
    def endpoint_name(self) -> str:
        return EndpointName.build_types

    def create_build_conf(self, build_type_id: str, project_id: str) -> tuple[Response, str]:
        payload = {
            'id': build_type_id,
            'name': (name := generate_faker_name()),
            'project': {
                'id': project_id
            },
            'steps': {
                'step': [
                    {
                        'name': 'Print hello world',
                        'type': 'simpleRunner',
                        'properties': {
                            'property': [
                                {
                                    'name': 'script.content',
                                    'value': 'echo \'Hello World!\''
                                },
                                {
                                    'name': 'teamcity.step.mode',
                                    'value': 'default'
                                },
                                {
                                    'name': 'use.custom.script',
                                    'value': 'true'
                                }
                            ]
                        }
                    }
                ]
            }
        }

        return self.post(payload), name

    def delete_build(self, build_type_id: str) -> Response:
        return self.delete(tail=f'/id:{build_type_id}')

    def get_build_info(self, build_type_id: str) -> Response:
        return self.get(tail=f'/id:{build_type_id}')


class TCBuildQueue(TCConnector):

    @property
    def endpoint_name(self) -> str:
        return EndpointName.build_queue

    def run_build(self, build_type_id: str) -> Response:
        payload = {
            'buildType': {
                'id': build_type_id
            }
        }
        return self.post(payload)

class TCUsers(TCConnector):

    @property
    def endpoint_name(self) -> str:
        return EndpointName.users

    def create_user(self, user: TeamcityUser,
                    role_name: str = Roles.system_admin, scope: str = 'g') -> Response:
        payload = {
            'username': user.username,
            'password': user.password
        }
        if role_name:
            payload.update({
                'roles':{
                    'role': [
                        {
                            'roleId': role_name,
                            'scope': scope,
                        }
                    ]
                }
            })
        return self.post(payload)

    def delete_user(self, user_id: int) -> Response:
        return self.delete(tail=f'/id:{user_id}')
