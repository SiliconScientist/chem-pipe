from ase.io import read, write
from mattersim.forcefield.potential import MatterSimCalculator
from mattersim.applications.relax import Relaxer
import torch
from chempipe.config import Config, get_config


def relax_potential(cfg: Config) -> None:
    contcar_path = cfg.vasp.output / "CONTCAR"
    best_model = cfg.fine_tune.checkpoints / "best_model.pth"
    if contcar_path.exists():
        atoms = read(contcar_path)
    else:
        atoms = read(cfg.input_path)
    if best_model.exists():
        load_path = str(best_model)
    else:
        load_path = str(cfg.potential.model_path)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    atoms.calc = MatterSimCalculator.from_checkpoint(load_path=load_path, device=device)
    # atoms.calc = MatterSimCalculator.from_checkpoint(load_path=load_path, device="cuda")
    relaxer = Relaxer(constrain_symmetry=False)
    _, atoms = relaxer.relax(
        atoms=atoms, fmax=cfg.potential.fmax, maxstep=cfg.potential.maxstep
    )
    write(
        filename=cfg.potential.relax_path,
        images=atoms,
        format="vasp",
    )


def main():
    cfg = get_config()
    cfg.init_paths()
    relax_potential(cfg=cfg)


if __name__ == "__main__":
    main()
