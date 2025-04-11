import json
from ase.io import read
from ase.calculators.vasp import Vasp

from chempipe.config import Config, get_config


def check_vasp_convergence(cfg: Config) -> bool:
    outcar_path = cfg.vasp.output / "OUTCAR"
    with open(outcar_path, "r") as f:
        for line in reversed(f.readlines()):
            if "reached required accuracy" in line:
                return True
    return False


def relax_vasp(cfg: Config) -> None:
    calc = Vasp(
        command=cfg.vasp.command,
        directory=cfg.vasp.output,
        **cfg.vasp.settings,
    )
    atoms = read(filename=cfg.potential.relaxed_path)
    atoms.calc = calc
    atoms.get_potential_energy()
    return check_vasp_convergence(cfg=cfg)


def write_convergence_status(converged: bool, checkpoint: str = "") -> None:
    status = {"converged": converged, "checkpoint": checkpoint or None}
    with open("status.json", "w") as f:
        json.dump(status, f, indent=2)
    print(f"📄 Wrote status.json: {status}")


def main():
    cfg = get_config()
    converged = relax_vasp(cfg)
    write_convergence_status(converged)


if __name__ == "__main__":
    main()
