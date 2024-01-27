from setuptools import setup, find_packages

setup(
    name="api",
    version="0.5",
    packages=find_packages(),
    provides=['services'],
    zip_safe=True
)