import json
import typing

class Config:

    def __init__(self, config_file_path: str = "config.json", default_config_file_path: str = "default_config.json"):
        self.config = {}
        self.default_config = {}
        self.config_file_path = config_file_path
        self.default_config_file_path = default_config_file_path
        
    def save(self) -> None:
        try:
            with open(self.config_file_path, 'w') as f:
                json.dump(self.config, f)
        except IOError as e:
            print(e)
        else:
            print('Config saved')


    def load(self) -> None:
        try:
            with open(self.config_file_path) as f:
                self.config = json.load(f)
        except IOError as e:
            print(e)
        else:
            print('Config loaded')

    def load_default_config_if_needed(self) -> None:
        if self.default_config != {}:
            return
        try:
            with open(self.default_config_file_path) as f:
                self.default_config = json.load(f)
        except IOError as e:
            print(e)
            raise e
            

    def get_value(self, server_id: int, key: str) -> typing.Any:
        if(str(server_id) in self.config):
            return self.config[str(server_id)][key]
        else:
            self.load_default_config_if_needed()
            self.config[str(server_id)] = self.default_config.copy()
            return 

        
    def set_value(self, server_id: int, key: str, value: typing.Any) -> None:
        if str(server_id) not in self.config:
            self.load_default_config_if_needed()
            self.config[str(server_id)] = self.default_config.copy()
        self.config[str(server_id)][key] = value
        self.save()