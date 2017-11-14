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

# Install
You can either use pip install or the setup.py script

```sh
pip install ramp-packer
```

```sh
python setup.py install
```

# Usage

## Manifest mode

```sh
ramp-packer <PATH_TO_RedisModule.so> -m <PATH_TO_Manifest.yml>
```

manifest.yml should specify your module's attributes, the ones you would specify manualy if you were to use
the Command line mode, see Full usage options and manifest.yml for a reference.

## Command line mode

```sh
ramp-packer <PATH_TO_RedisModule.so> -a <author> -e <email> -ar <architecture> -d <description> -ho <homepage> -l <license> -ex <extras> -c <cmdargs> -r <redis-min-version>
```

## Full usage options

```
Usage: ramp-packer [OPTIONS] MODULE

Options:
  -o, --output TEXT               output file name
  -v, --verbose                   verbose mode: print the resulting metadata
  -m, --manifest FILENAME         generate package from manifest
  -d, --display-name TEXT         name for display purposes
  -a, --author TEXT               module author
  -e, --email TEXT                author's email
  -A, --architecture TEXT         module compiled on i386/x86_64 arch
  -D, --description TEXT          short description
  -h, --homepage TEXT             module homepage
  -l, --license TEXT              license
  -c, --cmdargs TEXT              module command line arguments
  -r, --redis-min-version TEXT    redis minimum version
  -R, --redis-pack-min-version TEXT
                                  redis pack minimum version
  -O, --os TEXT                   build target OS (Darwin/Linux)
  -C, --capabilities TEXT         comma seperated list of module capabilities
  --help                          Show this message and exit.
```

For Help

```sh
ramp-packer -h
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
clustering | module is able to operate in a database that is sharded and shards can be migrated|

## Output
ramp-packer generates module.zip

Which contains:

    1. RedisModule.so - original module
    2. Module.json - module's metadata
