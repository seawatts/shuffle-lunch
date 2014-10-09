import os
from setuptools import setup

version_file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'version.txt'))
version = version_file.read().strip()

setup(
    name='shuffle_lunch',
    version=version,
    author='Chris Watts',
    author_email='chris.watts.t@gmail.com.com',
    url='https://github.com/seawatts/shuffle-lunch',
    scripts=['main.py']
)
