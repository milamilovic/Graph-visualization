from setuptools import setup, find_packages

setup(
    name="xml-loader",
    version="0.2",
    packages=find_packages(),
    entry_points={
        'loader':
        ['xml-loader=load_xml.load_xml:XmlLoader']
    },
    install_requires=["core>=0.1"],
    zip_safe=True
)