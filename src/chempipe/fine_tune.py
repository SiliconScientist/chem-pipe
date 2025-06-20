from ase.io import read, write
from types import SimpleNamespace
import os

os.environ["LOCAL_RANK"] = "0"
os.environ["RANK"] = "0"
os.environ["WORLD_SIZE"] = "1"
os.environ["MASTER_ADDR"] = "127.0.0.1"
os.environ["MASTER_PORT"] = "12355"
from mattersim.training import finetune_mattersim
import torch
from chempipe.config import Config, get_config
import os


# local_rank = int(os.environ.get("LOCAL_RANK", 0))
def get_fine_tune_args(cfg: Config):
    best_model = cfg.fine_tune.checkpoints / "best_model.pth"
    if best_model.exists():
        load_model_path = str(best_model)
    else:
        load_model_path = str(cfg.potential.model_path)
    args = SimpleNamespace(
        run_name="example",
        train_data_path=str(cfg.fine_tune.train_path),
        valid_data_path=str(cfg.fine_tune.train_path),
        load_model_path=load_model_path,
        save_path=str(cfg.fine_tune.checkpoints),
        save_checkpoint=True,
        ckpt_interval=50,
        # device="cuda",
        device="cuda" if torch.cuda.is_available() else "cpu",
        # model params
        cutoff=5.0,
        threebody_cutoff=4.0,
        # training params
        epochs=100,
        batch_size=16,
        lr=2e-4,
        step_size=20,
        include_forces=True,
        include_stresses=False,
        force_loss_ratio=1.0,
        stress_loss_ratio=0.1,
        early_stop_patience=10,
        seed=42,
        # scaling
        re_normalize=False,
        scale_key="per_species_forces_rms",
        shift_key="per_species_energy_mean_linear_reg",
        init_scale=None,
        init_shift=None,
        trainable_scale=False,
        trainable_shift=False,
        # wandb
        wandb=False,
        wandb_api_key=None,
        wandb_project="wandb_test",
    )
    return args


def fine_tune(cfg: Config) -> None:
    filename = cfg.vasp.output / "vasprun.xml"
    fine_tuning_atoms = read(filename=filename, index=":")
    write(
        filename=cfg.fine_tune.train_path,
        images=fine_tuning_atoms,
        format="extxyz",
    )
    args = get_fine_tune_args(cfg=cfg)
    finetune_mattersim.main(args)


def main():
    cfg = get_config()
    cfg.init_paths()
    fine_tune(cfg=cfg)


if __name__ == "__main__":
    main()
