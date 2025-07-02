import platform
import git.install as git_install
import helix.install as helix_install
import wezterm.install as wezterm_install
import powershell.install as powershell_install
import zsh.install as zsh_install


def main():
    print("Starting dotfiles installation...\n")

    name = input("Enter your real name for git: ")
    email = input("Enter you email for git: ")

    git_install.GitConfigInstaller(name, email).install()
    helix_install.install()
    wezterm_install.install()

    if platform.system() == "Windows":
        powershell_install.install()
    else:
        zsh_install.install()

    print("\nDotfiles installation complete!")


if __name__ == "__main__":
    main()
