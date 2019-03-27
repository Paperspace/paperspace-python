import io
import re
from codecs import open
from os import path

from setuptools import setup, find_packages

with io.open("paperspace/version.py", "rt", encoding="utf8") as f:
    version = re.search(r"version = \"(.*?)\"", f.read()).group(1)

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
try:
    import pypandoc

    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError, OSError):
    with open('README.md', encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='paperspace',
    version=version,
    description='Paperspace Python',
    long_description=long_description,
    url='https://github.com/paperspace/paperspace-python',
    author='Paperspace Co.',
    author_email='info@paperspace.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='paperspace api development library',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['requests[security]', 'boto3', 'botocore', 'six', 'gradient-statsd', 'click', 'terminaltables'],
    entry_points={'console_scripts': [
        'paperspace-python = paperspace.main:main',
    ]},
)
