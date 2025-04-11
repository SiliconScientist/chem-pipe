from pathlib import Path
from ase.io import read, write
from types import SimpleNamespace
from mattersim.training import finetune_mattersim

from chempipe.config import Config, get_config


def get_fine_tune_args(cfg: Config, train_data_path: Path):
    args = SimpleNamespace(
        run_name="example",
        train_data_path=train_data_path,
        valid_data_path=train_data_path,
        load_model_path=cfg.potential.model_path,
        save_path=cfg.fine_tune.checkpoints,
        save_checkpoint=True,
        ckpt_interval=50,
        device=cfg.device,
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
    fine_tuning_atoms = read(cfg.vasp.output / "OUTCAR", index=":")
    filename = cfg.vasp.output / "outcar.extxyz"
    write(
        filename=filename,
        images=fine_tuning_atoms,
        format="extxyz",
    )
    args = get_fine_tune_args(cfg=cfg, train_data_path=filename)
    finetune_mattersim.main(args)


def main():
    cfg = get_config()
    fine_tune(cfg=cfg)


if __name__ == "__main__":
    main()
