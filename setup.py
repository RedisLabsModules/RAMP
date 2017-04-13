from setuptools import setup, find_packages

setup(
    name='ramp-packer',
    version='1.0',
    description='Packs for Redis modules into a distributable format',
    author='RedisLabs',
    url='https://github.com/redislabs/RAMP',
    scripts=['packer/module_packer'],
    license='BSD 2-clause',
    long_description=open('README.md').read(),
    packages=find_packages(),
    install_requires=['redis']
)
