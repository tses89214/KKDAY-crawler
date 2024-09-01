import yaml

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        with open('config/config.yml', 'r') as file:
            self._config = yaml.safe_load(file)

    def get(self, key, default=None):
        return self._config.get(key, default)

config = Config()