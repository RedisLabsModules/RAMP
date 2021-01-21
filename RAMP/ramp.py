#!/usr/bin/env python

import os
import json
import click

from RAMP import config
from RAMP.packer import package
from RAMP.unpacker import unpack as unpack_bundle
from RAMP.version import VERSION
from .common import *


def comma_seperated_to_list(ctx, param, value):
    """
    Converts a comma seperated string into a list.
    """
    if value is None:
        return []
    else:
        items = value.split(',')
        return list(set(items))


def jsons_str_tuple_to_jsons_tuple(ctx, param, value):
    """
    Converts json str into python map
    """
    if value is None:
        return []
    else:
        return [json.loads(a) for a in value]


@click.group()
@click.version_option(version=VERSION)
def ramp():
    pass


@ramp.command()
def version():
    print('RAMP packer v={}'.format(str(VERSION)))
    return 0


@ramp.command()
@click.argument('bundle')
def validate(bundle):
    try:
        unpack(bundle)
        print("package is valid")
        return 0
    except Exception as e:
        eprint("package is invalid, reason: {}".format(e))
        return 1


@ramp.command()
@click.argument('bundle')
def unpack(bundle):
    metadata, module = unpack_bundle(bundle)
    module_metadata_file_name = os.path.join(os.getcwd(), metadata['module_name'] + '.json')
    module_file_name = os.path.join(os.getcwd(), metadata['module_file'])

    with open(module_metadata_file_name, 'w') as outfile:
        json.dump(metadata, outfile)
        print(module_metadata_file_name)

    with open(module_file_name, 'w') as outfile:
        for line in module.readlines():
            outfile.write(line)
        print(module_file_name)

    return 0


@ramp.command()
@click.argument('module')
@click.option('--manifest', '-m', type=click.File('rb'), help='generate package from manifest')
@click.option('--display-name', '-d', default=None, help='name for display purposes')
@click.option('--module-name', '-n', default=None, help='module name')
@click.option('--author', '-a', default=None, help='module author')
@click.option('--email', '-e', default=None, help='author\'s email')
@click.option('--architecture', '-A', default=None, help='module compiled on i386/x86_64 arch')
@click.option('--description', '-D', default=None, help='short description')
@click.option('--homepage', '-h', default=None, help='module homepage')
@click.option('--license', '-l', default=None, help='license')
@click.option('--cmdargs', '-c', 'command_line_args', default=None, help='module command line arguments')
@click.option('--runcmdargs', 'run_command_line_args', default=None, help='if set, use those args when running the redis server')
@click.option('--redis-min-version', '-r', 'min_redis_version', default=None, help='redis minimum version')
@click.option('--redis-pack-min-version', '-R', 'min_redis_pack_version', default=None, help='redis pack minimum version')
@click.option('--config-command', '-cc', default=None, help='command used to configure module args at runtime')
@click.option('--os', '-O', default=None, help='build target OS (Darwin/Linux)')
@click.option('--capabilities', '-C', callback=comma_seperated_to_list, help='comma seperated list of module capabilities')
@click.option('--exclude-commands', '-E', callback=comma_seperated_to_list, help='comma seperated list of exclude commands')
@click.option('--overide-command', multiple=True, callback=jsons_str_tuple_to_jsons_tuple, help='gets a command json representation and overide it on the module json file')
@click.option('--add-command', multiple=True, callback=jsons_str_tuple_to_jsons_tuple, help='gets a command json representation and add it on the module json file')
@click.option('--dependencies', callback=jsons_str_tuple_to_jsons_tuple, help='list of module dependencies: <name, uri, sha256>')
@click.option('--optional-dependencies', callback=jsons_str_tuple_to_jsons_tuple, help='list of module optional dependencies: <name, uri, sha256>')
@click.option('--output', '-o', default='module.zip', help='output file name')
@click.option('--print-filename-only', '-P', is_flag=True, default=False, help="Print package path, but don't generate file")
@click.option('--packname-file', default=None, help="Write package name to the file")
@click.option('--verbose', '-v', is_flag=True, default=False, help='verbose mode: print the resulting metadata')
@click.option('--debug', is_flag=True, default=False, help='Print interaction with Redis. Implies --verbose.')
def pack(module, *args, **kwargs):
    config.set(kwargs)
    return package(module, **kwargs)


if __name__ == '__main__':
    ramp()
