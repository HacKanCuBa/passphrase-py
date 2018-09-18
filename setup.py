#!/usr/bin/env python3

"""Passphrase installer script.

Install with `setup.py install`.

"""

from setuptools import setup
from passphrase.__main__ import __version__ as passphrase_version


def _readme():
    with open('README.rst') as rst:
        return rst.read()


setup(
    name='hc-passphrase',
    version=passphrase_version,
    description='Generates cryptographically secure passphrases and passwords',
    long_description=_readme(),
    classifiers=[
      'Development Status :: 5 - Production/Stable',
      'Environment :: Console',
      'Intended Audience :: Developers',
      'Intended Audience :: End Users/Desktop',
      'License :: OSI Approved :: GNU General Public License v3 or later '
      '(GPLv3+)',
      'Natural Language :: English',
      'Operating System :: POSIX :: Linux',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: 3.6',
      'Topic :: Security :: Cryptography',
      'Topic :: Utilities'
    ],
    platforms=[
      'POSIX :: Linux'
    ],
    keywords='cryptography passphrase password security',
    url='http://github.com/hackancuba/passphrase-py',
    download_url='https://github.com/HacKanCuBa/passphrase-py/archive/'
                 'v{}.tar.gz'.format(passphrase_version),
    author='HacKan',
    author_email='hackan@gmail.com',
    license='GNU GPL 3.0+',
    packages=['passphrase'],
    python_requires='>=3.5',
    install_requires=[
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    entry_points={
        'console_scripts': ['passphrase=passphrase.__main__:main'],
    },
    zip_safe=False
)
