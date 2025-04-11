from chempipe.config import Config


def check_vasp_convergence(cfg: Config) -> bool:
    outcar_path = cfg.vasp.output / "OUTCAR"
    with open(outcar_path, "r") as f:
        for line in reversed(f.readlines()):
            if "reached required accuracy" in line:
                return True
    return False
