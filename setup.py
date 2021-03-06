import os
import re
import sys
import codecs
from pathlib import Path
from setuptools import setup, find_packages, Extension
from setuptools.command.install import install


here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


VERSION = find_version('gentex', '__init__.py')


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')
        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(tag, VERSION)
            sys.exit(info)


# C extensions
comat = Extension('_libmakecomat',
                  sources=['gentex/makecomat.c'],
                  libraries=['m'])

# Read content of README file
with open(Path(here)/'README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='gentex',
    version=VERSION,
    description='General Texture Analysis',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='GenTex contributors',
    url='https://github.com/NPann/GenTex',
    packages=find_packages(exclude=('tests')),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Topic :: Scientific/Engineering :: Information Analysis'
    ],
    install_requires=[
        'numpy>=1.16',
        'Pillow>=6.1',
        'imageio>= 2.5.0',
        'scipy>=1.3',
    ],
    ext_modules=[comat],
    python_requires='>=3.7',
    cmdclass={
        'verify': VerifyVersionCommand,
    }
)
