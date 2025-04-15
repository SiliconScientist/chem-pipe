from pathlib import Path
from tomllib import load
from pydantic import BaseModel
from typing import Dict, Any


class Potential(BaseModel):
    model_path: Path
    relaxed_path: Path
    fmax: float


class Vasp(BaseModel):
    command: str
    output: Path
    settings: Dict[str, Any]


class FineTune(BaseModel):
    train_traj: Path
    checkpoints: Path


class Config(BaseModel):
    device: str
    input_structure: Path
    potential: Potential
    vasp: Vasp
    fine_tune: FineTune


def get_config():
    with open("config.toml", "rb") as f:
        cfg_data = load(f)
    return Config(**cfg_data)
