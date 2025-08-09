from setuptools import setup, find_packages

setup(
    name="my_module",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "my_module": ["templates/**/*", "templates/**/**/*"]
    },
    install_requires=["click"],
    entry_points={
        "console_scripts": [
            "myapi = my_module.cli:cli"
        ]
    }
)

