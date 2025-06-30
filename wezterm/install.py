from pathlib import Path
from scripts.common import link_or_copy

def install():
    home = Path.home()
    repo_root = Path(__file__).parent
    src = repo_root / "wezterm.lua"
    dest = home / ".wezterm.lua"

    print("Installing wezterm config...")
    link_or_copy(src, dest)
    print("WezTerm install complete.")

