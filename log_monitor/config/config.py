import sys
import yaml


def default_config():
    return {
        "log_file": "/tmp/access.log"
    }


def load_config(path):
    with open(path, "r") as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print("error when loading config file:", exc, file=sys.stderr)
            print("fallback to default configs", file=sys.stderr)
            return default_config()
