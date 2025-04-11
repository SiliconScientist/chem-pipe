from pathlib import Path
from tomllib import load
from pydantic import BaseModel
from typing import Dict, Any


class Paths(BaseModel):
    input_structure: Path
    ml_potential: Path


class Vasp(BaseModel):
    command: str
    directory: Path
    settings: Dict[str, Any]


class FineTune(BaseModel):
    potential: Path
    directory: Path


class Config(BaseModel):
    device: str
    paths: Paths
    vasp: Vasp
    fine_tune: FineTune


def get_config():
    with open("config.toml", "rb") as f:
        cfg_data = load(f)
    return Config(**cfg_data)
