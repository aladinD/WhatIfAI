# -*- coding: utf-8 -*-
# Maintainer: Niklas Landerer
# Copyright 2020 Lehrstuhl für Kommunikationsnetze
# SPDX-License-Identifier: Apache-2.0

"""TLS-gatherer project setup script"""

import io
import os
from setuptools import find_packages, setup


os.chdir(os.path.abspath(os.path.dirname(__file__)))


def read_requirements_in(path):
    """Read requirements from requirements.in file.
    """
    with io.open(path, 'rt', encoding='utf8') as file:  # pylint: disable=redefined-outer-name
        return [
            x.rsplit('=')[1] if x.startswith('-e') else x
            for x in [x.strip() for x in file.readlines()]
            if x
            if not x.startswith('-r')
            if not x[0] == '#'
        ]


INSTALL_REQUIRES = read_requirements_in('dependencies/requirements.in')


setup(name='TLS-gatherer',
      version='0.0.0',
      description='A docker based system gathering pcap traces',
      license='Apache-2.0',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      python_requires='>=3.7.0',
      install_requires=INSTALL_REQUIRES,
      setup_requires=[
          'pytest-runner',
      ],
      entry_points={
          'console_scripts': ['supervisor = src.garthering_supervisor:run_supervisor'],
      })
