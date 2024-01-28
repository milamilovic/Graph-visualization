from setuptools import setup, find_packages

setup(
    name="json-loader",
    version="0.2",
    packages=find_packages(),
    entry_points={
        'loader':
        ['json-loader=load_json.load_json:JsonLoader']
    },
    install_requires=["core>=0.1"],
    zip_safe=True
)