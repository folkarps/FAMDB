from distutils.core import setup

setup(
    name='FAMDB',
    version='2.1.1',
    url='https://github.com/folkarps/FAMDB',
    install_requires=[
        'passlib',
        'psutil',
        'pycryptodome',
        'requests',
    ],
    license='MIT',
    author='abarton',
    author_email='Raptoer@gmail.com',
    description='Folk ARPS Arma mission database'
)
