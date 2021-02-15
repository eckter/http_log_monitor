import sys
import yaml
from pathlib import Path


def default_config() -> dict:
    """ Generates the default configuration dict

    It reads the config file at the root of the repository
    :return: default configuration dict
    """
    root = Path(__file__).parent
    default_config_path = root / "config_default.yml"
    with open(default_config_path, "r") as f:
        return yaml.safe_load(f)


def load_config(path: str) -> dict:
    """ Loads the given config file (yaml is expected)
    On error, a warning is displayed and the default config file is used instead

    :param path: path to the config file
    :return: configuration dict
    """
    with open(path, "r") as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print("error when loading config file:", exc, file=sys.stderr, flush=True)
            print("fallback to default configs", file=sys.stderr, flush=True)
            return default_config()
