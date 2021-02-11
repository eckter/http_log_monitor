import sys
import yaml
from pathlib import Path


def default_config() -> dict:
    root = Path(__file__).parents[2]
    default_config_path = root / "config_default.yml"
    with open(default_config_path, "r") as f:
        return yaml.safe_load(f)


def load_config(path: str) -> dict:
    with open(path, "r") as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print("error when loading config file:", exc, file=sys.stderr)
            print("fallback to default configs", file=sys.stderr)
            return default_config()
