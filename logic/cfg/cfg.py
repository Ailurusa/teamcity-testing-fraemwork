from pathlib import Path

from yaml import load, Loader

CFG_LOCATION = 'resources/config.yaml'


class Config:
    """Singleton configuration keeper"""

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self._raw_data = self.__read_cfg_file()

    def __read_cfg_file(self):
        if hasattr(self, '_raw_data'):
            return self._raw_data
        return load(self.cfg_file.open(), Loader=Loader)

    @property
    def cfg_file(self):
        location = Path(__file__).parent.parent / CFG_LOCATION
        assert location.exists(), f'Config file not found. Expected location: {location}'
        return location

    @property
    def host_with_token(self):
        return f'http://:{self.super_user_token}@{self.server_ip}:{self.port}'

    @property
    def host(self):
        return f'http://{self.server_ip}:{self.port}'

    @property
    def port(self):
        return self.__get_cfg_attr('port')

    @property
    def server_ip(self):
        return self.__get_cfg_attr('server_ip')

    @property
    def super_user_token(self):
        return self.__get_cfg_attr('super_user_token')

    def __get_cfg_attr(self, attr_name: str):
        if attr_name not in self._raw_data:
            raise AttributeError(f'Next attribute not found in config file: {attr_name}')
        return self._raw_data[attr_name]
