# chem-pipe
Atomic simulation pipeline utilizing quantum calculations and ML interatomic potentials

# LONI Setup:
- On LONI, in your scratch directory (i.e. `/scratch/$USER`), create a directory for your GitHub repositories: `mkdir github`
- Inside your `github` directory, clone this repository:
    ```
    git clone https://github.com/SiliconScientist/chem-pipe.git
    ```
- Load the following python module: `module load python/3.9.7-anaconda`
- Inside the `chemp-pipe` directory, create a virtual environment using the `uv` dependency manager:
    - `uv venv .venv`
    - `source .venv/bin/activate --python=python`
    - `uv pip install -r requirement.txt`
- In your home directory, add the following lines to your `.bashrc` file:
    ```
    alias cpenv='source /scratch/$USER/github/chem-pipe/.venv/bin/activate'
    export UV_CACHE_DIR=/scratch/$USER/.cache/uv
    export VASP_SCRIPT=/home/$USER/vasp/run_vasp.py
    export VASP_PP_PATH=/home/$USER/vasp/mypps
    ```
- To activate the new contents of your `.bashrc` file, run `source .bashrc`.
- Add VASP scripts (e.g. vasp_std, vasp_gam, etc.) into your `/home/$USER/vasp/vaspbin/' directory.
- Add VASP pseudopotentials into your `/home/$USER/vasp/mypps/' directory.

Congratulations! You'll never have to do that part again!

### Job submission:
- Create a directory anywhere on LONI: `mkdir project1`.
- Add a `config.toml` file to your project, which you can do ways:
    - Copy it from `~/chem-pipe/config.example.toml` and rename it.
    - Copy an old `config.toml` from a previous chem-pipe project.

- Customize your configuration file with your `#SBATCH` specifications and VASP parameters.
- Add a structure file (i.e. `POSCAR`) to your directory so your project looks like this directory tree:
    ```
    test/
    ├── config.toml
    └── POSCAR
    ```
- Activate the chempipe environment with the `cpenv` alias
- From your `project1` directory, run `python -m chempipe`


