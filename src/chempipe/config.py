from pathlib import Path
from tomllib import load
from pydantic import BaseModel


class Paths(BaseModel):
    input: Path


class Config(BaseModel):
    paths: Paths


def get_config():
    with open("config.toml", "rb") as f:
        cfg_data = load(f)
    return Config(**cfg_data)
