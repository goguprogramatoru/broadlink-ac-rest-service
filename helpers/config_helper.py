import yaml
import sys
import os

class ConfigHelper:

    yaml_config = None

    server_bind_address = "0.0.0.0"
    server_port = 9000

    service_secret = ""

    def __init__(self):
        base_folder = sys.path[0]
        path_full = os.path.join(base_folder, "config.yaml")
        with open(path_full, 'r') as f:
            try:
                yaml_content = yaml.safe_load(f)
                self.yaml_config = yaml_content
            except yaml.YAMLError:
                print(f'Error. Invalid yaml format in config file')

        self.server_bind_address = self.yaml_config["server"]["bind_address"]
        self.server_port = int(self.yaml_config["server"]["port"])
        self.service_secret = self.yaml_config["service"]["secret"]
