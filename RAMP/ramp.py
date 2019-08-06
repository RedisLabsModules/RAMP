#!/usr/bin/env python

import os
import json
import click

from RAMP.packer import package
from RAMP.unpacker import validate_bundle, unpack as unpack_bundle
from RAMP.version import VERSION
import RAMP.module_metadata as module_metadata

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
        return [json.loads(a) for  a in value]

@click.group()
def ramp():
    pass

@ramp.command()
def version():
    print('RAMP packer v={}'.format(str(VERSION)))
    return 0

@ramp.command()
@click.argument('bundle')
def validate(bundle):
    valid, e = validate_bundle(bundle)
    if valid:
        print("package is valid")
        return 0
    else:
        print("package is invalid, reason: %s" % e)
    return 1

@ramp.command()
@click.argument('bundle')
def unpack(bundle):
    metadata, module = unpack_bundle(bundle)
    module_metadata_file_name = os.path.join(os.getcwd(), metadata['module_name']+'.json')
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
@click.option('--output', '-o', default='module.zip', help='output file name')
@click.option('--verbose', '-v', is_flag=True, help='verbose mode: print the resulting metadata')
@click.option('--manifest', '-m', type=click.File('rb'), help='generate package from manifest')
@click.option('--display-name', '-d', 'display_name', default=module_metadata.DISPLAY_NAME, help='name for display purposes')
@click.option('--module-name', '-n', 'module_name', help='module name')
@click.option('--author', '-a', default=module_metadata.AUTHOR, help='module author')
@click.option('--email', '-e', default=module_metadata.EMAIL, help='author\'s email')
@click.option('--architecture', '-A', default=module_metadata.ARCHITECTURE, help='module compiled on i386/x86_64 arch')
@click.option('--description', '-D', default=module_metadata.DESCRIPTION, help='short description')
@click.option('--homepage', '-h', default=module_metadata.HOMEPAGE, help='module homepage')
@click.option('--license', '-l', default=module_metadata.LICENSE, help='license')
@click.option('--cmdargs', '-c', default=module_metadata.COMMAND_LINE_ARGS, help='module command line arguments')
@click.option('--redis-min-version', '-r', 'redis_min_version', default=module_metadata.MIN_REDIS_VERSION, help='redis minimum version')
@click.option('--redis-pack-min-version', '-R', 'redis_pack_min_version', default=module_metadata.MIN_REDIS_PACK_VERSION, help='redis pack minimum version')
@click.option('--config-command', '-cc', default=module_metadata.CONFIG_COMMAND, help='command used to configure module args at runtime')
@click.option('--os', '-O', default=module_metadata.OS, help='build target OS (Darwin/Linux)')
@click.option('--capabilities', '-C', callback=comma_seperated_to_list, help='comma seperated list of module capabilities')
@click.option('--print-filename-only', '-P', is_flag=True, help="Print package path, but don't generate file")
@click.option('--exclude-commands', '-E', callback=comma_seperated_to_list, help='comma seperated list of exclude commands')
@click.option('--overide-command', multiple=True, callback=jsons_str_tuple_to_jsons_tuple, help='gets a command json representation and overide it on the module json file')
def pack(module, output, verbose, manifest, display_name, module_name, author,
         email, architecture, description, homepage, license, cmdargs,
         redis_min_version, redis_pack_min_version, config_command, os, capabilities,
         print_filename_only, exclude_commands, overide_command):
    return package(module, output, verbose, manifest, display_name, module_name, author,
                   email, architecture, description, homepage, license, cmdargs,
                   redis_min_version, redis_pack_min_version, config_command, os, capabilities,
                   print_filename_only, exclude_commands, overide_command)

if __name__ == '__main__':
    ramp()
