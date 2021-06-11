"""Root."""
from setuptools import setup, find_packages

setup(
    test_suite='tests',
    name='website',
    version='0.2.0',
    packages=find_packages(include=['website', 'website.*'])
)
