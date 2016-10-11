from distutils.core import setup

setup(
    name='FAMDB',
    version='1',
    packages=[''],
    package_dir={'': 'python'},
    url='https://github.com/Raptoer/FAMDB',
    license='',
    author='abarton',
    author_email='Raptoer@gmail.com',
    description='Arma mission database',
    install_requires=[
        'passlib',
        'pycrypto'
    ]
)
