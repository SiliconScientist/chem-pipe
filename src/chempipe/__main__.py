from ase.io import read
from ase.calculators.vasp import Vasp
from mattersim.forcefield.potential import MatterSimCalculator
from mattersim.applications.relax import Relaxer

from chempipe.config import get_config
from chempipe.relax import check_vasp_convergence
from chempipe.fine_tune import fine_tune


def main():
    cfg = get_config()
    atoms = read(cfg.input_structure)
    dft_calc = Vasp(
        command=cfg.vasp.command, directory=cfg.vasp.output, **cfg.vasp.settings
    )
    relaxer = Relaxer()
    converged = False
    while not converged:
        # ML relaxation
        atoms.calc = MatterSimCalculator(potential=cfg.potential, device=cfg.device)
        # We don't check for convergence with the ML potential
        _, atoms = relaxer.relax(atoms=atoms)
        # DFT relaxation
        atoms.calc = dft_calc
        atoms.get_potential_energy()
        converged = check_vasp_convergence(cfg=cfg)
        if converged:
            print("DFT relaxation converged.")
        else:
            cfg = fine_tune(cfg=cfg)


if __name__ == "__main__":
    main()
