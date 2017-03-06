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
## Interactive mode

```sh
python module_packer <PATH_TO_RedisModule.so>
```

## Command line mode

```sh
python module_packer <PATH_TO_RedisModule.so> -a <author> -e <email> -ar <architecture> -d <description> -ho <homepage> -l <license> -ex <extras> -c <cmdargs> -r <redis-min-version>
```

For Help

```sh
python module_packer <PATH_TO_RedisModule.so> -h
```

## Output
module_packer generates module.zip

Which contains:
    
    1. RedisModule.so - original module
    2. Module.json - module's metadata
