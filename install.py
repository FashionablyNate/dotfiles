import git.install as git_install
# import helix.install as helix_install
# import wezterm.install as wezterm_install
# import zsh.install as zsh_install

def main():
    print("Starting dotfiles installation...\n")

    name = input("Enter your real name: ")
    email = input("Enter you email: ")
    
    git_install.install(name, email)
    # helix_install.install()
    # wezterm_install.install()
    # zsh_install.install()

    print("\nDotfiles installation complete!")

if __name__ == "__main__":
    main()
