__author__ = 'julien.lefevre'
from setuptools import setup

setup(
    name="qi",
    version="0.1.1",
    author="Julien LEFEVRE",
    description="A tool to execute same request on multiple servers in parallel. Needs to be autorized by keys.",
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