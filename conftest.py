import pytest

from logic.api.connection import TCUsers, TCProjects, TCBuildTypes
from logic.models.api import TeamcityUser
from logic.utils import generate_guid_str


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "description(text): describe a test"
    )


@pytest.fixture(scope='function')
def build_type_id() -> str:
    build_type_id = generate_guid_str('build')
    yield build_type_id
    TCBuildTypes().delete_build(build_type_id)


@pytest.fixture(scope='function')
def project_id() -> str:
    project_id = generate_guid_str('project')
    yield project_id
    TCProjects().delete_project(project_id)


@pytest.fixture(scope='function')
def two_project_ids() -> list[str]:
    ids = [generate_guid_str('project'), generate_guid_str('project')]
    yield ids
    for id_ in ids:
        TCProjects().delete_project(id_)


@pytest.fixture(scope='function')
def user() -> TeamcityUser:
    user = TeamcityUser()
    yield user
    if user.id:
        TCUsers().delete_user(user.id)
