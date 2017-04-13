from setuptools import setup, find_packages

setup(
    name='RAMP',
    version='1.0',
    description='Packs for Redis modules into a distributable format',
    author='RedisLabs',
    url='https://github.com/redislabs/RAMP',
    scripts=['packer/module_packer'],
    license='AGPL-3.0',
    long_description=open('README.txt').read(),
    packages=find_packages(),
    install_requires=['redis']
)