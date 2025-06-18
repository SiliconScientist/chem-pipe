import os
from pathlib import Path
import shutil
from pydantic import BaseModel
from typing import Dict, Any, Optional

try:
    from tomllib import load  # Python 3.11+
except ImportError:
    from toml import load  # External backport for Python <3.11


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
    relax_path: Optional[Path] = None
    fmax: float


class Vasp(BaseModel):
    script: str
    output: Optional[Path] = None
    settings: Dict[str, Any]


class FineTune(BaseModel):
    train_path: Optional[Path] = None
    checkpoints: Optional[Path] = None


class MainConfig(BaseModel):
    data: Path


class Config(BaseModel):
    main: MainConfig
    input_path: Optional[Path] = None
    potential: Potential
    vasp: Vasp
    fine_tune: Optional[FineTune] = None

    def init_paths(self) -> None:
        base = self.main.data
        base.mkdir(parents=True, exist_ok=True)

        # 1. Create all required directories
        if self.fine_tune is None:
            self.fine_tune = FineTune()
        (base / "ml_relax").mkdir(parents=True, exist_ok=True)
        (base / "vasp_output").mkdir(parents=True, exist_ok=True)
        (base / "fine_tune" / "checkpoints").mkdir(parents=True, exist_ok=True)
        (base / "input_structure").mkdir(parents=True, exist_ok=True)

        # 2. Handle POSCAR: move/copy into input_structure
        original_poscar = Path("POSCAR")
        self.input_path = base / "input" / "POSCAR"

        if original_poscar.exists():
            # Move or copy POSCAR into data/input_structure
            if not self.input_path.exists():
                shutil.move(original_poscar, self.input_path)
        else:
            print("Warning: POSCAR not found in working directory.")

        # 3. Build all other paths
        self.potential.relax_path = base / "ml_relax" / "CONTCAR"
        self.vasp.output = base / "vasp_output"
        self.fine_tune.train_path = base / "fine_tune" / "train.extxyz"
        self.fine_tune.checkpoints = base / "fine_tune" / "checkpoints"

        # 4. VASP command
        if self.vasp.script:
            self.vasp.script = (
                f"mpirun /home/{os.getenv('USER')}/vasp/vaspbin/{self.vasp.script}"
            )
        else:
            self.vasp.script = f"mpirun /home/{os.getenv('USER')}/vasp/vaspbin/vasp_std"


def get_config():
    with open("config.toml", "r") as f:
        cfg_data = load(f)
    return Config(**cfg_data)
