from ase.io import read
from mattersim.applications.relax import Relaxer

from chempipe.config import get_config


def main():
    cfg = get_config()
    atoms = read(cfg.paths.input)
    relaxer = Relaxer()


if __name__ == "__main__":
    main()
