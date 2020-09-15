#!/usr/bin/env python
from setuptools import find_packages, setup
from taxi_tempo import __version__

install_requires = [
    'taxi>=6.0',
    'requests>=2.3.0',
]

setup(
    name='taxi_tempo',
    version=__version__,
    packages=find_packages(),
    description='Tempo backend for Taxi',
    author='Alexandre Blin',
    author_email='alexandre@blin.fr',
    url='https://github.com/alexandreblin/taxi-tempo',
    install_requires=install_requires,
    license='wtfpl',
    python_requires=">=3.6",
    entry_points={
        'taxi.backends': 'tempo = taxi_tempo.backend:TempoBackend'
    },
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
