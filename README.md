# chem-pipe
Atomic simulation pipeline utilizing quantum calculations and ML interatomic potentials

# LONI Setup:
- Add VASP scripts (e.g. vasp_std, vasp_gam, etc.) into your `/home/$USER/vasp/vaspbin/' directory.
- Add VASP pseudopotentials into your `/home/$USER/vasp/mypps/' directory.
- On LONI, inside your `.bashrc` file:
    ```
    export UV_CACHE_DIR=/scratch/$USER/.cache/uv
    export VASP_SCRIPT=/home/$USER/vasp/run_vasp.py
    export VASP_PP_PATH=/home/$USER/vasp/mypps
    ```
- In your `/scratch/$USER/Github/` directory, clone this repository:
    ```
    git clone https://github.com/SiliconScientist/chem-pipe.git
    ```
- Clone the MatterSim repository into your `/scratch/$USER/Github/` directory.
- In this repo, build your virtual environment:
    1) uv venv .venv
    2) source .venv/bin/activate
    3) uv pip install -r requirements.txt
- Setup a directory scheme according to this diagram: #TODO: Make this more elegant/consolidate?
    ```
    data/
    ├── POSCAR                        # Initial structure for ML relaxation
    ├── ml_relaxed/
    ├── fine_tune/
    │   └── checkpoints/              # Directory where model checkpoints are saved
    vasp_output/                      # Directory for all VASP-generated outputs
    ```
- Modify your config.toml file according to your directory scheme and user specifications.

### Job submission:
```
bash pipeline.sh 
```
