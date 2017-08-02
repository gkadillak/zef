from setuptools import setup, find_packages

setup(
    name='zenfetch',
    author='Garrett Kadillak',
    author_email='gkadillak@gmail.com',
    url='https://github.com/gkadillak/zenfetch',
    packages=find_packages(),
    description='A simple command line tool for '
    'fetching information about your sprint from Zenhub',
    version='0.1',
    install_requires=[
        'Click',
        'Requests',
    ],
    entry_points={
        'console_scripts': [
            'zef = zenfetch.command_line:cli'
        ]
    }

)
