from setuptools import setup, find_packages

setup(
    name="rdf-loader",
    version="0.2",
    packages=find_packages(),
    entry_points={
        'loader':
        ['rdf-loader=load_rdf.load_rdf:RDFLoader']
    },
    install_requires=["core>=0.1"],
    zip_safe=True
)