from pathlib import Path
from scripts.common import link_or_copy

def install():
    home = Path.home()
    repo_root = Path(__file__).parent
    src = repo_root / "zshrc"
    dest = home / ".zshrc"

    print("Installing zsh config...")
    link_or_copy(src, dest)
    print("Zsh install complete.")
