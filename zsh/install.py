from pathlib import Path
from scripts.common import link_or_copy


def install():
    src = Path(__file__).parent
    dest = Path.home()

    print("Installing zsh config...")
    link_or_copy(src / "zshrc", dest / ".zshrc")
    link_or_copy(src / "p10k.zsh", dest / ".p10k.zsh")
    print("Zsh install complete.")
