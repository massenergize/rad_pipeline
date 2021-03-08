"""The setup script."""

from setuptools import find_packages
from setuptools import setup
from typing import List
from pathlib import Path

NAME = "rad_pipeline"
PACKAGES = find_packages()
META_PATH = Path("rad_pipeline") / "__init__.py"
HERE = Path(__file__).absolute().parent

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

INSTALL_REQUIRES = (HERE/"requirements.txt").read_text().split("\n") # type: List[str]

SETUP_REQUIRES = ['pytest-runner',]

TEST_REQUIRES = ['pytest>=3',]

setup(
    author="Alex Hasha",
    author_email='ahasha@gmail.com',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="MassEnergize Renewable Actions Dataset Pipeline",
    entry_points={
        'console_scripts': [
            'rad=rad_pipeline.cli:main',
        ],
    },
    install_requires=INSTALL_REQUIRES,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='rad_pipeline',
    name='rad_pipeline',
    packages=find_packages(include=['rad_pipeline']),
    setup_requires=SETUP_REQUIRES,
    test_suite='tests',
    tests_require=TEST_REQUIRES,
    url='https://github.com/ahasha/rad_pipeline',
    version='0.1.0',
    zip_safe=False,
)
