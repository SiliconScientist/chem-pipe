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


def relax_vasp(cfg: Config) -> bool:
    calc = Vasp(
        command=cfg.vasp.script,
        directory=str(cfg.vasp.output),
        **cfg.vasp.settings,
    )
    atoms = read(filename=cfg.potential.relax_path, format="vasp")
    atoms.calc = calc
    try:
        atoms.get_potential_energy()
    except Exception as e:
        print(f"[ERROR] VASP calculation failed: {e}")
        return False
    return check_vasp_convergence(cfg=cfg)


def write_convergence_status(converged: bool) -> None:
    status = {"converged": converged}
    with open("status.json", "w") as f:
        json.dump(status, f, indent=2)
    print(f"Wrote status.json: {status}")


def main():
    cfg = get_config()
    converged = relax_vasp(cfg)
    write_convergence_status(converged)


if __name__ == "__main__":
    main()
