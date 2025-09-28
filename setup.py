from setuptools import setup, find_packages

setup(
    name="zenpo",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "zenpo=zenpo.cli:main"
        ]
    },
    install_requires=[
        "pyfiglet",
        "colorama"
    ],
    python_requires=">=3.7",
    description="A general control panel CLI tool",
    author="Zenpo",
    url="https://github.com/ZC-RS/zenpo",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "Environment :: Console"
    ]
)
