from setuptools import setup, find_packages
from adiumsh import __version__
import platform


if platform.python_version() < '3':
    requirements = open('requirements.txt').read().splitlines()
else:
    requirements = open('requirements-3.txt').read().splitlines()

setup(
    name='adium-sh',
    version=__version__,
    description='Command-line wrapper of Adium',
    long_description=open('README.rst').read(),
    keywords='adium',
    author='Shichao An',
    author_email='shichao.an@nyu.edu',
    url='https://github.com/shichao-an/adium-sh',
    license='BSD',
    install_requires=requirements,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    package_data={
        'adiumsh': ['*.scpt'],
    },
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'adiumsh = adiumsh.adiumsh:main',
        ],
    },
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
)
