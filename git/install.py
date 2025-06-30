import subprocess
import tempfile
import os
import textwrap
from pathlib import Path
from scripts.common import link_or_copy


def install(name: str, email: str):
    home = Path.home()
    repo_root = Path(__file__).parent
    src_gitconfig = repo_root / "gitconfig"
    dest_gitconfig = home / ".gitconfig"

    print("Checking for Git signing key in .gitconfig...")
    key = get_git_signing_key()
    if not key:
        print("No Git signing key set, checking local GPG keys...")
        key = get_gpg_secret_keys()
        if not key:
            print("No signing key found in local GPG keys, generating one...")
            generate_gpg_key(name, email)
            key = get_gpg_secret_keys()

    write_gitconfig_local(repo_root, name, email, key)

    print("Installing git config...")
    link_or_copy(src_gitconfig, dest_gitconfig)

    print("Git install complete.")


def write_gitconfig_local(
    repo_root: Path, name: str, email: str, signingkey: str | None
):
    user_content = textwrap.dedent(f"""
        [user]
            name = {name}
            email = {email}
    """)
    gpg_content = textwrap.dedent(f"""
            signingkey = {signingkey}
        [commit]
            gpgsign = true
        [gpg]
            program = gpg
    """)
    with open(repo_root / "gitconfig", "w") as dest_f:
        with open(repo_root / "gitconfig.global", "r") as default_f:
            for line in default_f.readlines():
                dest_f.write(line)
        dest_f.write(user_content.strip() + "\n")
        if signingkey:
            dest_f.write("    " + gpg_content.strip() + "\n")


def get_git_signing_key():
    """Get signing key from git config if set."""
    try:
        key = subprocess.check_output(
            ["git", "config", "--get", "user.signingkey"], text=True
        ).strip()
        if key:
            return key
    except subprocess.CalledProcessError:
        pass
    return None


def get_gpg_secret_keys():
    """List secret GPG keys and return the first key ID found."""
    try:
        output = subprocess.check_output(
            ["gpg", "--list-secret-keys", "--keyid-format=long"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
        # Parse output to find key IDs
        # The line with key looks like:
        # sec   rsa4096/ABCDEF1234567890 2020-01-01 [SC]
        for line in output.splitlines():
            line = line.strip()
            if line.startswith("sec"):
                # Example: sec   rsa4096/ABCDEF1234567890 2020-01-01 [SC]
                parts = line.split()
                if len(parts) > 1:
                    key_part = parts[1]  # rsa4096/ABCDEF1234567890
                    if "/" in key_part:
                        return key_part.split("/")[1]
    except subprocess.CalledProcessError:
        pass
    return None


def save_signing_key_to_dotfile(key, filepath):
    """Append or update the signing key in a dotfile (e.g., .gitconfig or your custom config)."""
    # For example, appending to ~/.gitconfig is one option, or a custom file
    with open(filepath, "a") as f:
        f.write(f"\n[user]\n\tsigningkey = {key}\n")


def generate_gpg_key(name, email):
    batch_content = f"""
%no-protection
Key-Type: default
Key-Length: 4096
Subkey-Type: default
Subkey-Length: 4096
Name-Real: {name}
Name-Email: {email}
Expire-Date: 0
%commit
"""
    # Write the batch file to a temp file
    with tempfile.NamedTemporaryFile("w", delete=False) as batch_file:
        batch_file.write(batch_content)
        batch_path = batch_file.name

    try:
        subprocess.run(["gpg", "--batch", "--generate-key", batch_path], check=True)
        print("GPG key generated successfully.")
    finally:
        os.remove(batch_path)
