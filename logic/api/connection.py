from abc import ABC, abstractmethod

from requests import Session

from logic.cfg import Config
from logic.models.api import TeamcityUser, EndpointName
from logic.utils import generate_faker_name


class TCConnector(ABC):
    def __init__(self):
        self.session = Session()
        self.session.auth = TeamcityUser().credentials

    @property
    def url(self):
        return f'{Config().host}/app/rest/{self.endpoint_name}'

    @property
    @abstractmethod
    def endpoint_name(self) -> str:
        raise NotImplemented

    def post(self, payload: dict):
        return self.session.post(self.url, json=payload)


class TCProjects(TCConnector):

    @property
    def endpoint_name(self) -> str:
        return EndpointName.projects

    def create(self, project_id):
        payload = {
            'parentProject': {
                'locator': '_Root'
            },
            'name': generate_faker_name(),
            'id': project_id,
            'copyAllAssociatedSettings': True
        }
        return self.post(payload)


class TCBuildTypes(TCConnector):

    @property
    def endpoint_name(self) -> str:
        return EndpointName.build_types

    def create_build_conf(self, build_type_id, project_id):
        payload = {
            'id': build_type_id,
            'name': 'Print hello world',
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

        return self.post(payload)


class TCBuildQueue(TCConnector):

    @property
    def endpoint_name(self) -> str:
        return EndpointName.build_queue

    def run_build(self, build_type_id):
        payload = {
            'buildType': {
                'id': build_type_id
            }
        }
        return self.post(payload)
