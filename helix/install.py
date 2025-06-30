from pathlib import Path
from scripts.common import link_or_copy

def install():
    home = Path.home()
    repo_root = Path(__file__).parent
    src_config = repo_root / "config.toml"
    dest_config = home / ".config" / "helix" / "config.toml"

    print("Installing helix config...")
    link_or_copy(src_config, dest_config)
    print("Helix install complete.")

