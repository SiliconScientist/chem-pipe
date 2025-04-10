from ase.io import read
from ase.calculators.vasp import Vasp
from mattersim.forcefield.potential import MatterSimCalculator
from mattersim.applications.relax import Relaxer

from chempipe.config import get_config


def main():
    cfg = get_config()
    atoms = read(cfg.paths.input)
    vasp_calc = Vasp(
        command=cfg.vasp.command, directory=cfg.vasp.directory, **cfg.vasp.settings
    )
    atoms.calc = vasp_calc
    atoms.get_potential_energy()
    # mattersim_calc = MatterSimCalculator()
    # relaxer = Relaxer()
    # converged, atoms = relaxer.relax(atoms=atoms)
    # print(f"Relaxation converged: {converged}")


if __name__ == "__main__":
    main()
