[![license](https://img.shields.io/github/license/RedisLabsModules/RAMP.svg)](https://github.com/RedisLabsModules/RAMP)
[![CircleCI](https://circleci.com/gh/RedisLabsModules/RAMP/tree/master.svg?style=svg)](https://circleci.com/gh/RedisLabsModules/RAMP/tree/master)
[![GitHub issues](https://img.shields.io/github/release/RedisLabsModules/RAMP.svg)](https://github.com/RedisLabsModules/RAMP/releases/latest)
[![Codecov](https://codecov.io/gh/RedisLabsModules/RAMP/branch/master/graph/badge.svg)](https://codecov.io/gh/RedisLabsModules/RAMP)


# RAMP

Redis Automatic Module Packaging

Similar to `npm init`, this packer bundles Redis Modules for later distribution.

It gathers information from modules e.g.
module's name, command list, version and additional metadata.

## Prerequisites

Make sure redis-server is on your PATH

```sh
export PATH=$PATH:<PATH_TO_REDIS>
```

## Install

You can either use pip install or the setup.py script

```sh
pip install ramp-packer
```

```sh
python setup.py install
```

## Usage

## Manifest mode

```sh
ramp pack <PATH_TO_RedisModule.so> -m <PATH_TO_Manifest.yml>
```

manifest.yml should specify your module's attributes, the ones you would specify manualy if you were to use
the Command line mode, see Full usage options and manifest.yml for a reference.

## Command line mode

```sh
ramp pack <PATH_TO_RedisModule.so> -a <author> -e <email> -A <architecture> -d <description> -h <homepage> -l <license> -c <cmdargs> -r <redis-min-version>
```

## Full usage options

```sh
Usage: ramp [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  pack
  unpack
  validate
  version
```

## Packing

```sh
Usage: ramp pack [OPTIONS] MODULE

Options:
  -o, --output TEXT               output file name
  -v, --verbose                   verbose mode: print the resulting metadata
  -m, --manifest FILENAME         generate package from manifest
  -d, --display-name TEXT         name for display purposes
  -a, --author TEXT               module author
  -e, --email TEXT                authors email
  -A, --architecture TEXT         module compiled on i386/x86_64 arch
  -D, --description TEXT          short description
  -h, --homepage TEXT             module homepage
  -l, --license TEXT              license
  -c, --cmdargs TEXT              module command line arguments
  -r, --redis-min-version TEXT    redis minimum version
  -R, --redis-pack-min-version TEXT
                                  redis pack minimum version
  -cc, --config-command TEXT      command to configure module at run time

  -O, --os TEXT                   build target OS (Darwin/Linux)
  -C, --capabilities TEXT         comma seperated list of module capabilities
  --help                          Show this message and exit.
```

## Module Capabilities

Following is a list of capabilities which can be specified for a module

capability | description |
---------- | ----------- |
types | module has its own types and not only operate on existing redis types|
no_multi_key | module has no methods that operate on multiple keys|
replica_of | module can work with replicaof capability when it is loaded into a source or a destination database|
backup_restore | module can work with import/export capability|
eviction_expiry | module is able to handle eviction and expiry without an issue|
reshard_rebalance | module is able to operate in a database that is resharded and rebalanced|
failover_migrate | module is able to operate in a database that is failing over and migrating|
persistence_aof | module is able to operate in a database when database chooses AOF persistence option|
persistence_rdb | module is able to operate in a database when database chooses SNAPSHOT persistence option|
hash_policy | module is able to operate in a database with a user defined HASH POLICY|
flash | module is able to operate in a database with Flash memory is enabled or changed over time|
crdb | module is able to operate in a database with crdt for the default redis data types|    
clustering | module is able to operate in a database that is sharded and shards can be migrated|
intershard_tls | module supports two-way encrypted communication between shards|

## Output

ramp pack generates module.zip

Which contains:

    1. RedisModule.so - original module
    2. Module.json - module's metadata

## Test
Make sure redis-server is on your PATH

```sh
export PATH=$PATH:<PATH_TO_REDIS>
```

Install RAMP
```sh
python setup.py install
```

Compile RedisGraph for your OS v1.0.12 (https://github.com/RedisLabsModules/RedisGraph/tree/v1.0.12)

Copy `redisgraph.so` in `test_module` directory in the root of this project.

Run tests
```sh
python test.py
```
