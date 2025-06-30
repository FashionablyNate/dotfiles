from pathlib import Path
import shutil
import sys
from scripts.common import link_or_copy


def install():
    documents = Path.home() / "Documents" / "PowerShell"
    profile_path = documents / "Microsoft.PowerShell_profile.ps1"

    repo_root = Path(__file__).parent
    src_profile = repo_root / "powershell" / "Microsoft.PowerShell_profile.ps1"

    documents.mkdir(parents=True, exist_ok=True)

    if profile_path.exists():
        backup_path = profile_path.with_suffix(".ps1.bak")
        print(f"Backing up existing profile to {backup_path}")
        shutil.copy(profile_path, backup_path)

    link_or_copy(src_profile, profile_path)

    print(f"Installed PowerShell profile to {profile_path}")
