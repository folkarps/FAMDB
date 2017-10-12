from distutils.core import setup

setup(
    name='FAMDB',
    version='2.1',
    url='https://github.com/Raptoer/FAMDB',
    install_requires=[
        'discord.py',
        'passlib',
        'pycrypto',
        'psutil',
    ],
    license='MIT',
    author='abarton',
    author_email='Raptoer@gmail.com',
    description='Arma mission database'
)
