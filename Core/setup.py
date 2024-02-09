from setuptools import setup, find_packages

setup(
    name="core",
    version="0.5",
    packages=find_packages(),
    provides=['use_cases', 'models'],
    zip_safe=True
)