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
## Interactive mode

```sh
python module_packer <PATH_TO_RedisModule.so>
```

## Command line mode

```sh
python module_packer <PATH_TO_RedisModule.so> -a <author> -e <email> -ar <architecture> -d <description> -ho <homepage> -l <license> -ex <extras> -c <cmdargs> -r <redis-min-version>
```

## Full usage options

```
usage: module_packer [-h] [-o OUTFILE] [-v] [-i]
                     [-a AUTHOR | -e EMAIL | -ar ARCHITECTURE | -d DESCRIPTION | -ho HOMEPAGE | -l LICENSE | -ex EXTRA_FILES | -c COMMAND_LINE_ARGS | -r REDIS_MIN_VERSION | -rl RLEC_MIN_VERSION | -O OS]
                     MODULE

Create a new module package

positional arguments:
  MODULE

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILE, --output OUTFILE
                        Output file name
  -v, --verbose         Verbose mode: print the resulting metadata
  -i, --interactive
  -a AUTHOR, --author AUTHOR
                        module author
  -e EMAIL, --email EMAIL
                        author's email
  -ar ARCHITECTURE, --architecture ARCHITECTURE
                        module compiled on i386/x86_64 arch
  -d DESCRIPTION, --description DESCRIPTION
                        short description
  -ho HOMEPAGE, --homepage HOMEPAGE
                        module homepage
  -l LICENSE, --license LICENSE
                        license
  -ex EXTRA_FILES, --extras EXTRA_FILES
                        extra files
  -c COMMAND_LINE_ARGS, --cmdargs COMMAND_LINE_ARGS
                        module command line arguments
  -r REDIS_MIN_VERSION, --redis-min-version REDIS_MIN_VERSION
                        redis minimum version
  -rl RLEC_MIN_VERSION, --rlec-min-version RLEC_MIN_VERSION
                        rlec minimum version
  -O OS, --os OS        Build target OS (Darwin/Linux)
```

For Help

```sh
python module_packer  -h
```

## Output
module_packer generates module.zip

Which contains:
    
    1. RedisModule.so - original module
    2. Module.json - module's metadata
