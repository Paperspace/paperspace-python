from codecs import open
from os import path
from setuptools import setup, find_packages

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
    version='0.0.12',
    description='Paperspace Python',
    long_description=long_description,
    url='https://github.com/paperspace/paperspace-python',
    author='Paperspace Co.',
    author_email='info@paperspace.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='paperspace api development library',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['requests[security]', 'boto3', 'botocore', 'six'],
    entry_points={'console_scripts': [
        'paperspace-python = paperspace.main:main',
    ]},
)
