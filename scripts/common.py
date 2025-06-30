import os
import platform
from pathlib import Path
import shutil

def is_windows():
    return platform.system() == "Windows"

def link_or_copy(src: Path, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() or dest.is_symlink():
        dest.unlink()
    try:
        if is_windows():
            try:
                os.symlink(src, dest)
                print(f"Symlinked {dest} -> {src}")
            except (OSError, NotImplementedError):
                if src.is_dir():
                    shutil.copytree(src, dest)
                else:
                    shutil.copy2(src, dest)
                print(f"Copied {dest} -> {src}")
        else:
            os.symlink(src, dest)
            print(f"Symlinked {dest} -> {src}")
    except Exception as e:
        print(f"Failed to link or copy {dest}: {e}")

