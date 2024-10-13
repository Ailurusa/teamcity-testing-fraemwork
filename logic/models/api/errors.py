from dataclasses import dataclass


@dataclass
class APIErrors:
    access_denied_user_permissions = 'You do not have enough permissions to edit project'
