from setuptools import setup, find_packages
from RAMP.version import VERSION

LONG_DESC = """
# RAMP
Redis Automatic Module Packaging

Similar to `npm init`, this packer bundles Redis Modules for later distribution.

It gathers information from modules e.g.
module's name, command list, version and additional metadata.

# Prerequisites
Make sure redis-server is on your PATH

```sh
export PATH=$PATH:<PATH_TO_REDIS>
```

# Usage

## Command line mode

```sh
ramp <PATH_TO_RedisModule.so> -a <author> -e <email> -ar <architecture> -d <description> -ho <homepage> -l <license> -ex <extras> -c <cmdargs> -r <redis-min-version>
```

For Help

```sh
ramp -h
```

## Output
ramp generates module.zip

Which contains:

    1. RedisModule.so - original module
    2. Module.json - module's metadata

"""

setup(
    name='ramp-packer',
    py_modules=['RAMP'],
    version=str(VERSION),
    description='Packs for Redis modules into a distributable format',
    author='RedisLabs',
    url='https://github.com/redislabs/RAMP',
    download_url='https://github.com/RedisLabs/RAMP/archive/{}.tar.gz'.format(VERSION),
    license='BSD 2-clause',
    long_description=LONG_DESC,
    packages=find_packages(),
    install_requires=['redis<=2.10.6', 'pyyaml', 'click>=6.7', 'semantic_version==2.6.0', 'typing'],
    entry_points='''
        [console_scripts]
        ramp=RAMP.ramp:ramp
    ''',
)
