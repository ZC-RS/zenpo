from setuptools import setup, find_packages

setup(
    name="zenpo",
    version="1.2.6",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "zenpo=zenpo:main"
        ]
    },
    install_requires=[
        "pyfiglet",
        "colorama"
    ],
    python_requires=">=3.7",
)
