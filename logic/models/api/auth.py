from dataclasses import dataclass
from logic.cfg import Config

@dataclass
class TeamcityUser:
    username = Config().username
    password = Config().password

    @property
    def credentials(self):
        return self.username, self.password
