__author__ = 'julien.lefevre'
from setuptools import setup

setup(
    name="qi",
    version="0.1",
    author="Julien LEFEVRE",
    author_email="julien.lefevr@gmail.com",
    packages=['qi'],
    py_modules=['main', 'config', 'command'],
    install_requires=['paramiko', 'argparse'],
    entry_points= {
        'console_scripts': [
            'qi = qi.main:main'
        ]
    }
)