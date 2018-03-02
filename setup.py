try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name = 'vmwarebackuper',
    version = '1.0.5',
    author = 'lucas-ed2017',
    author_email = 'dddsimonddd@hotmail.com',
    url = 'https://github.com/lucas-ed2017',
    license='GPLv3',
    packages=['vmwarebackuper'],
    description = 'A module to backup VMs inside a VMWare eSXi\'s host.',
    )
