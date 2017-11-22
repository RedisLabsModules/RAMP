import os
import json
import zipfile
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

def package(module, output, verbose, manifest, display_name, author,
            email, architecture, description, homepage, license, cmdargs,
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
