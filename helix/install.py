from pathlib import Path
from scripts.common import link_or_copy


def install():
    home = Path.home()
    repo_root = Path(__file__).parent
    src_config = repo_root
    dest_config = home / ".config" / "helix"

    print("Installing helix config...")
    link_or_copy(src_config / "config.toml", dest_config / "config.toml")
    link_or_copy(src_config / "languages.toml", dest_config / "languages.toml")
    print("Helix install complete.")
