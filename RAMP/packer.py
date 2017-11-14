import os
import json
import zipfile
import click
import yaml
import semantic_version

import RAMP.module_metadata as module_metadata
from RAMP.commands_discovery import discover_modules_commands

def version_to_semantic_version(version):
    """
    Creates a semantic version from a numeric redis module version.
    """

    major = int(version / 10000)
    version -= major * 10000
    minor = int(version / 100)
    version -= minor * 100
    patch = int(version)

    sem_version_str = '{}.{}.{}'.format(major, minor, patch)
    # sem_version_str = '%02d.%02d.%02d' % (major, minor, patch)
    return semantic_version.Version(sem_version_str)

def set_defaults(module_path):
    """
    Creates a module metadata using default values
    """
    metadata = module_metadata.create_default_metadata(module_path)
    return metadata

def manifest_mode(metadata, manifest):
    """
    Creates module metadata from user provided menifest file
    """
    try:
        data = yaml.load(manifest)
        for key, val in data.iteritems():
            if key in metadata:
                metadata[key] = val
            else:
                print'{} unknow attribute'.format(key)
    except yaml.YAMLError as exc:
        print exc

def archive(module_path, metadata, archive_name='module.zip'):
    """
    Archives both module and module metadata.
    """
    archive_name = archive_name.format(**metadata)
    with open('module.json', 'w') as outfile:
        json.dump(metadata, outfile, indent=4, sort_keys=True)

    archive_file = zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED)
    try:
        archive_file.write(module_path, metadata["module_file"])
        archive_file.write('module.json')
        print archive_name
    finally:
        archive_file.close()
        os.remove("module.json")

def comma_seperated_to_list(ctx, param, value):
    """
    Converts a comma seperated string into a list.
    """
    if value is None:
        return []
    else:
        items = value.split(',')
        return list(set(items))

@click.command()
@click.argument('module')
@click.option('--output', '-o', default='module.zip', help='output file name')
@click.option('--verbose', '-v', is_flag=True, help='verbose mode: print the resulting metadata')
@click.option('--manifest', '-m', type=click.File('rb'), help='generate package from manifest')
@click.option('--display-name', '-d', 'display_name', default=module_metadata.DISPLAY_NAME, help='name for display purposes')
@click.option('--author', '-a', default=module_metadata.AUTHOR, help='module author')
@click.option('--email', '-e', default=module_metadata.EMAIL, help='author\'s email')
@click.option('--architecture', '-A', default=module_metadata.ARCHITECTURE, help='module compiled on i386/x86_64 arch')
@click.option('--description', '-D', default=module_metadata.DESCRIPTION, help='short description')
@click.option('--homepage', '-h', default=module_metadata.HOMEPAGE, help='module homepage')
@click.option('--license', '-l', default=module_metadata.LICENSE, help='license')
@click.option('--cmdargs', '-c', default=module_metadata.COMMAND_LINE_ARGS, help='module command line arguments')
@click.option('--redis-min-version', '-r', 'redis_min_version', default=module_metadata.MIN_REDIS_VERSION, help='redis minimum version')
@click.option('--redis-pack-min-version', '-R', 'redis_pack_min_version', default=module_metadata.MIN_REDIS_PACK_VERSION, help='redis pack minimum version')
@click.option('--os', '-O', default=module_metadata.OS, help='build target OS (Darwin/Linux)')
@click.option('--capabilities', '-C', callback=comma_seperated_to_list, help='comma seperated list of module capabilities')
def package(module, output, verbose, manifest, display_name, author, email,
            architecture, description, homepage, license, cmdargs,
            redis_min_version, redis_pack_min_version, os, capabilities):
    module_path = module
    metadata = set_defaults(module_path)

    if manifest:
        manifest_mode(metadata, manifest)
    else:
        metadata["architecture"] = architecture
        metadata["os"] = os
        metadata["display_name"] = display_name
        metadata["author"] = author
        metadata["email"] = email
        metadata["description"] = description
        metadata["homepage"] = homepage
        metadata["license"] = license
        metadata["command_line_args"] = cmdargs
        metadata["min_redis_version"] = redis_min_version
        metadata["min_redis_pack_version"] = redis_pack_min_version
        metadata["capabilities"] = capabilities

    # Load module into redis and discover its commands
    module = discover_modules_commands(module_path, metadata["command_line_args"])
    metadata["module_name"] = module.name
    metadata["version"] = module.version
    metadata["semantic_version"] = str(version_to_semantic_version(module.version))
    metadata["commands"] = [cmd.to_dict() for cmd in module.commands]

    if verbose:
        print "Module Metadata:"
        print json.dumps(metadata, indent=2)

    archive(module_path, metadata, archive_name=output)
    return 0
