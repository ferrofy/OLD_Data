from setuptools import setup, find_packages

setup(
    name="ferrofy",
    version="0.2.0.1",
    packages=find_packages(),
    description="FerroFy Library",
    author="FerroFy | Vikrant Pathania",
    author_email="team.ferrofy@gmail.com",
    url="https://github.com/ferrofy/Library",
    install_requires=[
        "qrcode[pil]"
    ]
)