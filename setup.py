from distutils.core import setup

setup(
    name='FAMDB',
    version='2',
    package_dir={'': ''},
    url='https://github.com/Raptoer/FAMDB',
    license='',
    author='abarton',
    author_email='Raptoer@gmail.com',
    description='Arma mission database',
    packages=[
        'passlib',
        'pycrypto',
        'psutil'
    ]
)
