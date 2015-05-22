#!/usr/bin/env python

from setuptools import setup

setup(
	name='loyaltybay',
	version='0.1.0',
	description='API wrapper for LoyaltyBay',
	author='Nick Snell',
	author_email='nick@boughtbymany.com',
	license='BSD',
	url='https://boughtbymany.com',
	packages=[
		'loyaltybay',
	],
	install_requires=[
		'requests'
	]
)