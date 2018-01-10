# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
	readme= f.read()

setup(
	name='pyElegant',
	version='0.1.0',
	description='python modules for interfacing with Elegant',
	long_description=readme,
	author='Ryan Roussel',
	author_email='roussel@ucla.edu',
	packages=find_packages(exclude=('tests', 'docs'))
)
