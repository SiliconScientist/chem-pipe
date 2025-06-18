import sys
import chempipe
import subprocess
from pathlib import Path
from chempipe.config import get_config


def main():
    cfg = get_config()  # Load the config
    cfg.init_paths()  # Create folders from config
    package_dir = Path(chempipe.__file__).parent.parent.parent
    script_path = package_dir / "pipeline.sh"
    if not script_path.exists():
        print(f"Error: pipeline.sh not found at {script_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Running {script_path}...")
    try:
        subprocess.run(["bash", str(script_path)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"pipeline.sh failed with exit code {e.returncode}", file=sys.stderr)
        sys.exit(e.returncode)


if __name__ == "__main__":
    main()
