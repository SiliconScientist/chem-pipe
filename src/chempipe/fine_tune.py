from ase.io import read, write
from types import SimpleNamespace
from mattersim.training import finetune_mattersim

from chempipe.config import Config, get_config


def get_fine_tune_args(cfg: Config):
    args = SimpleNamespace(
        run_name="example",
        train_data_path=str(cfg.fine_tune.train_traj),
        valid_data_path=str(cfg.fine_tune.train_traj),
        load_model_path=str(
            cfg.potential.model_path
        ),  # TODO: We should check if there is another checkpoint available, and use that as the load_model_path
        save_path=str(cfg.fine_tune.checkpoints),
        save_checkpoint=True,
        ckpt_interval=50,
        device="cuda",
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
        filename=cfg.fine_tune.train_traj,
        images=fine_tuning_atoms,
        format="extxyz",
    )
    args = get_fine_tune_args(cfg=cfg)
    finetune_mattersim.main(args)


def main():
    cfg = get_config()
    fine_tune(cfg=cfg)


if __name__ == "__main__":
    main()
