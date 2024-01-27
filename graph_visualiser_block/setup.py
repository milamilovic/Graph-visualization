from setuptools import setup, find_packages

setup(
    name="block-visualizer",
    version="0.2",
    packages=find_packages(),
    entry_points={
        'visualizer':
        ['block-visualizer=block_visualiser.block_visualiser:BlockVisualiser']
    },
    install_requires=["core>=0.1"],
    zip_safe=True
)