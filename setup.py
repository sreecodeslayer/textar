from setuptools import setup

setup(
    name='textar', version='1.0',
    description='Textar is a simple and readable archive format',
    author='Sreenadh TC', author_email='kesav.tc8@gmail.com',
    packages=['textar'], entry_points={'console_scripts': ['textar = textar.cli:cli']},
    zip_safe=False
)
