from setuptools import setup

setup(
    name="dotfiles",
    version="0.1.0",
    py_modules=["install"],
    entry_points={
        "console_scripts": [
            "dotfiles-install=install:main",
        ],
    },
)

