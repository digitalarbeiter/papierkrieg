from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name="papierkrieg",
    version="0.0.1",
    description="tools for organizing bureaucratic documents",
    license="LGPLv3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="digitalarbeiter",
    author_email="digitalarbeiter@digitalbriefkasten.de",
    url="https://github.com/digitalarbeiter/papierkrieg",
    packages=["papierkrieg"],
    install_requires=[
        "click",
        "pyenchant",
        "requests",
        "pyocr",
        "Pillow",
        "probspellchecker",
    ],
    scripts=[
        "pkrieg-import-scan.py",
        "pkrieg-delete-index.py",
    ]
)
