from pathlib import Path
from tomllib import load
from pydantic import BaseModel
from typing import Dict, Any


class SBATCHConfig(BaseModel):
    job_name: str
    account: str
    partition: str
    nodes: int
    ntasks: int
    time: str
    email_user: str
    email_type: str


class Potential(BaseModel):
    model_path: Path
    relax_path: Path
    fmax: float


class Vasp(BaseModel):
    command: str
    output: Path
    settings: Dict[str, Any]


class FineTune(BaseModel):
    train_path: Path
    checkpoints: Path


class Config(BaseModel):
    input_path: Path
    potential: Potential
    vasp: Vasp
    fine_tune: FineTune


def get_config():
    with open("config.toml", "rb") as f:
        cfg_data = load(f)
    return Config(**cfg_data)
