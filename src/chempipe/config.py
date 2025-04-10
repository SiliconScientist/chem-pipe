from pathlib import Path
from tomllib import load
from pydantic import BaseModel
from typing import Dict, Any


class Paths(BaseModel):
    input: Path


class Vasp(BaseModel):
    command: str
    directory: Path
    settings: Dict[str, Any]


class Config(BaseModel):
    paths: Paths
    vasp: Vasp


def get_config():
    with open("config.toml", "rb") as f:
        cfg_data = load(f)
    return Config(**cfg_data)
