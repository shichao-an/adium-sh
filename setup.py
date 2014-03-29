from setuptools import setup, find_packages
from adiumsh import __version__


setup(
    name='adium-sh',
    version=__version__,
    description='Command-line wrapper of Adium',
    long_description=open('README.rst').read(),
    keywords='adium',
    author='Shichao An',
    author_email='shichao.an@nyu.edu',
    url='https://github.com/shichao-an/adiumsh',
    license='BSD',
    install_requires=['argparse', 'psutil'],
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
