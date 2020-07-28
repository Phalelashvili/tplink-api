from setuptools import setup, find_packages

version = "0.1"

setup(
    name="tplink-api",
    version=version,
    description="TP-Link Router API Wrapper",
    author="Spartak Phalelashvili",
    author_email="phalelashvili@protonmail.com",
    license="MIT",
    packages=find_packages(),
    url="https://github.com/Phalelashvili/tplink_api",
    install_requires=[
        "requests",
    ],
)
