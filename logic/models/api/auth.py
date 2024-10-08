from logic.utils import generate_faker_name


class TeamcityUser:
    def __init__(self):
        self.username = generate_faker_name()
        self.password = generate_faker_name()
        self.id: int | None = None

    @property
    def credentials(self) -> tuple[str, str]:
        return self.username, self.password

    def set_id(self, user_id: int) -> None:
        self.id = user_id
