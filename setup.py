#!/usr/bin/env python
import os

from setuptools import setup
from setuptools import find_packages


def add_requirements(file_path):
    """ Reads a requirements.txt file and returns a list of strings for all
    package names in this file.
    """
    with open(os.path.join(os.path.dirname(__file__), file_path)) as req_file:
        return [package_name.strip() for package_name in req_file]

# Get whatever in README.md and assign it to the `long_description` var.
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    long_description = f.read()

version = '0.1'

sdict = {
    'name': 'bottleful',
    'version': version,
    'description': 'Small library to simplify RESTful API creation with Bottle',
    'long_description': long_description,
    'packages': find_packages(exclude=['tests']),
    'include_package_data': True,
    'zip_safe': False,
    'test_suite': "tests",

    # We need this option to be able to specify the `install_component` argument
    # Example:
    # python setup.py develop install_component development
    'setup_requires': [
        'distribute-install_component',
    ],

    # That's going to be installed with the normal `setup.py install`
    'install_requires': add_requirements('requirements/base.txt'),

    # List of package names to be used with `install_component`
    'extras_require': {
        'development': add_requirements('requirements/development.txt'),
    },
}

setup(**sdict)
