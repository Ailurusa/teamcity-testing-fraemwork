from uuid import uuid4

from faker import Faker


def generate_guid_str(prefix: str | None = None) -> str:
    """
    Generate random str value using uuid4 function

    :param prefix: Optional static str prefix before generate id
    :return: result as [prefix]_id
    """

    random_id = str(uuid4())
    return random_id if not prefix else f'{prefix}_{random_id}'


def generate_faker_text(max_length: int = 20) -> str:
    """Generate text using Faker lib"""

    return Faker().text(max_length)

def generate_faker_name() -> str:
    """Generate name using Faker lib"""

    return Faker().name()
