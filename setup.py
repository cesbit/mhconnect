"""setup.py
python setup.py sdist
twine upload --repository pypitest dist/mhconnect-x.x.x.tar.gz
twine upload --repository pypi dist/mhconnect-x.x.x.tar.gz
"""
from setuptools import setup, find_packages
from mhconnect import __version__ as version
from setuptools import setup, find_packages

try:
    with open('README.md', 'r') as f:
        long_description = f.read()
except IOError:
    long_description = ''

setup(
    name='mhconnect',
    packages=find_packages(),
    version=version,
    description='MessageHub Connector',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cesbit/mhconnect',
    download_url=(
        'https://github.com/cesbit/'
        'mhconnect/tarball/v{}'.format(version)),
    keywords=['connector', 'oversight', 'messagehub'],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic'
    ],
)
