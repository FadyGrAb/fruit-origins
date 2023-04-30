from setuptools import setup, find_packages

setup(
    name="modelutils",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Click", "pytest", "tensorflow"],
    entry_points={
        "console_scripts": ["mutils = modelutils:cli"],
    },
)
