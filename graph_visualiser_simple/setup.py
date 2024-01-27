from setuptools import setup, find_packages

setup(
    name="simple-visualizer",
    version="0.2",
    packages=find_packages(),
    entry_points={
        'visualizer':
        ['simple-visualizer=simple_visualiser.simple_visualiser:SimpleVisualiser']
    },
    install_requires=["core>=0.1"],
    zip_safe=True
)