import yaml
from typing import Dict, Any
import os

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def load_config(file_name: str = "config.yml"):
    config_path = os.path.join(root_dir, file_name)

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config
