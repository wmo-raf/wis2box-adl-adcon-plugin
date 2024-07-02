#!/usr/bin/env python
import os

from setuptools import find_packages, setup

PROJECT_DIR = os.path.dirname(__file__)
REQUIREMENTS_FILE = os.path.join(PROJECT_DIR, "requirements.txt")
VERSION = "0.0.1"


def get_requirements():
    with open(REQUIREMENTS_FILE) as fp:
        return [
            x.strip()
            for x in fp.read().split("\n")
            if not x.strip().startswith("#") and not x.strip().startswith("-")
        ]


install_requires = get_requirements()

setup(
    name="wis2box-adl-adcon-plugin",
    version=VERSION,
    url="TODO",
    author="Erick Otenyo",
    author_email="otenyo.erick@gmail.com",
    license="MIT",
    description="WIS2Box Automated Data Loader - ADCON Plugin",
    long_description="TODO",
    platforms=["linux"],
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    install_requires=install_requires,
)
