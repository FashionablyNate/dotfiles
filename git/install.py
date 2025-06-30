import subprocess
import tempfile
import os
import textwrap
import logging
from pathlib import Path
from scripts.common import link_or_copy

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


class GitConfigInstaller:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.home = Path.home()
        self.repo_root = Path(__file__).parent
        self.src_gitconfig = self.repo_root / "gitconfig"
        self.dest_gitconfig = self.home / ".gitconfig"

    def install(self):
        logger.info("Checking for Git signing key in .gitconfig...")
        key = self.get_git_signing_key()

        if not key:
            logger.info("No Git signing key found, checking local GPG keys...")
            key = self.get_gpg_secret_key()

            if not key:
                logger.info("No local GPG keys found, generating new key...")
                key = self.generate_gpg_key()

        self.write_gitconfig_local(key)

        logger.info("Installing git config...")
        link_or_copy(self.src_gitconfig, self.dest_gitconfig)
        logger.info("Git config installation complete.")

    def write_gitconfig_local(self, signingkey: str | None):
        user_content = textwrap.dedent(f"""
            [user]
                name = {self.name}
                email = {self.email}
        """)

        gpg_content = ""
        if signingkey:
            gpg_content = textwrap.dedent(f"""
                signingkey = {signingkey}
            [commit]
                gpgsign = true
            [gpg]
                program = gpg
            """)

        dest_path = self.repo_root / "gitconfig"
        global_path = self.repo_root / "gitconfig.global"

        try:
            with open(dest_path, "w") as dest_f, open(global_path, "r") as global_f:
                dest_f.writelines(global_f.readlines())
                dest_f.write(user_content.strip() + "\n")
                if signingkey:
                    dest_f.write("    " + gpg_content.strip() + "\n")
        except Exception as e:
            logger.error(f"Failed to write gitconfig: {e}")
            raise

    def get_git_signing_key(self) -> str | None:
        try:
            key = subprocess.check_output(
                ["git", "config", "--get", "user.signingkey"], text=True
            ).strip()
            return key if key else None
        except subprocess.CalledProcessError:
            logger.debug("No signing key set in git config.")
            return None
        except Exception as e:
            logger.error(f"Error checking git signing key: {e}")
            return None

    def get_gpg_secret_key(self) -> str | None:
        try:
            output = subprocess.check_output(
                ["gpg", "--list-secret-keys", "--keyid-format=long"],
                text=True,
                stderr=subprocess.DEVNULL,
            )
            for line in output.splitlines():
                line = line.strip()
                if line.startswith("sec"):
                    parts = line.split()
                    if len(parts) > 1 and "/" in parts[1]:
                        return parts[1].split("/")[1]
        except subprocess.CalledProcessError:
            logger.debug("No secret keys found with GPG.")
        except Exception as e:
            logger.error(f"Error listing GPG keys: {e}")
        return None

    def generate_gpg_key(self) -> str:
        batch_content = textwrap.dedent(f"""
            %no-protection
            Key-Type: default
            Key-Length: 4096
            Subkey-Type: default
            Subkey-Length: 4096
            Name-Real: {self.name}
            Name-Email: {self.email}
            Expire-Date: 0
            %commit
        """)

        with tempfile.NamedTemporaryFile("w", delete=False) as batch_file:
            batch_file.write(batch_content)
            batch_path = batch_file.name

        try:
            subprocess.run(["gpg", "--batch", "--generate-key", batch_path], check=True)
            logger.info("GPG key generated successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to generate GPG key: {e}")
            raise
        finally:
            try:
                os.remove(batch_path)
            except OSError as e:
                logger.warning(f"Failed to remove temporary batch file: {e}")

        # Retrieve the new key
        key = self.get_gpg_secret_key()
        if not key:
            raise RuntimeError("Failed to retrieve newly generated GPG key.")
        return key
