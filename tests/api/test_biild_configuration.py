import allure
import pytest

from conftest import build_type_id, project_id, user, two_project_ids
from logic.api.connection import TCUsers, TCProjects, TCBuildTypes
from logic.models.api import APIErrors, Roles
from logic.utils import check_error_message, check_status


class TestBuildType:

    @pytest.mark.description('User should be able to create build type')
    @pytest.mark.positive
    def test_user_creates_build_type(self, user, project_id, build_type_id):
        with allure.step('Create user'):
            response = TCUsers().create_user(user)
            check_status(response)
            user.set_id(response.json().get('id'))

        with allure.step('Create project by user'):
            response = TCProjects(user).create(project_id)
            check_status(response)

        with allure.step('Create buildType for project by user'):
            builds_manager = TCBuildTypes(user)
            response, build_name = builds_manager.create_build_conf(build_type_id, project_id)
            check_status(response)

        with allure.step('Check buildType was created successfully with correct data'):
            assert builds_manager.get_build_info(build_type_id).json().get('name') == build_name

    @pytest.mark.description('User should not be able to create two build types with the same id')
    @pytest.mark.negative
    def test_user_creates_two_build_types_with_the_same_id(self, user, project_id, build_type_id):
        with allure.step('Create user'):
            response = TCUsers().create_user(user)
            check_status(response)
            user.set_id(response.json().get('id'))

        with allure.step('Create project by user'):
            response = TCProjects(user).create(project_id)
            check_status(response)

        with allure.step('Create buildType1 for project by user'):
            builds_manager = TCBuildTypes(user)
            response, build_name = builds_manager.create_build_conf(build_type_id, project_id)
            check_status(response)

        with allure.step('Create buildType2 for project by user'):
            builds_manager = TCBuildTypes(user)
            response, build_name = builds_manager.create_build_conf(build_type_id, project_id)

        with allure.step('Check buildType2 was not created with bad request code'):
            check_status(response, expected_code=400)

    @pytest.mark.description('Project admin should be able to create build type for their project')
    @pytest.mark.positive
    def test_project_admin_creates_build_type(self, user, project_id, build_type_id):
        with allure.step('Create project'):
            response = TCProjects().create(project_id)
            check_status(response)

        with allure.step('Create user with PROJECT_ADMIN role in a project created on previous step'):
            user_manager = TCUsers()
            response = user_manager.create_user(user, Roles.project_admin, f'p:{project_id}')
            check_status(response)
            user.set_id(response.json().get('id'))

        with allure.step('Create buildType for project by user'):
            builds_manager = TCBuildTypes(user)
            response, build_name = builds_manager.create_build_conf(build_type_id, project_id)

        with allure.step('Check buildType was created successfully'):
            check_status(response)

    @pytest.mark.description('Project admin should not be able to create build type for not their project')
    @pytest.mark.negative
    def test_project_admin_creates_build_type_for_another_user_project(self, user, two_project_ids, build_type_id):
        with allure.step('Create project #1'):
            response = TCProjects().create(two_project_ids[0])
            check_status(response)

        with allure.step('Create user with PROJECT_ADMIN role in a project created on previous step'):
            user_manager = TCUsers()
            response = user_manager.create_user(user, Roles.project_admin, f'p:{two_project_ids[0]}')
            check_status(response)
            user.set_id(response.json().get('id'))

        with allure.step('Create project #2'):
            response = TCProjects().create(two_project_ids[1])
            check_status(response)

        with allure.step('Create buildType for project2 by user'):
            builds_manager = TCBuildTypes(user)
            response, build_name = builds_manager.create_build_conf(build_type_id, two_project_ids[1])

        with allure.step('Check buildType was not created with forbidden code'):
            check_status(response, expected_code=403)
            check_error_message(response, APIErrors.access_denied_user_permissions)
