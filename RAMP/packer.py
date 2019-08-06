import os
import json
import zipfile
import yaml
import semantic_version

import RAMP.module_metadata as module_metadata
from RAMP.commands_discovery import discover_modules_commands
from subprocess import Popen, PIPE

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
        for key, val in data.items():
            if key in metadata:
                metadata[key] = val
            else:
                print('{} unknow attribute'.format(key))
    except yaml.YAMLError as exc:
        print(exc)


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
        print(archive_name)
    finally:
        archive_file.close()
        os.remove("module.json")

def package(module, output, verbose, manifest, display_name, module_name, author,
            email, architecture, description, homepage, license, cmdargs,
            redis_min_version, redis_pack_min_version, config_command, os, capabilities,
            print_filename_only, exclude_commands, overide_command):
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
        metadata["config_command"] = config_command
        metadata["exclude_commands"] = exclude_commands
        metadata["overide_command"] = overide_command

    # Load module into redis and discover its commands
    module = discover_modules_commands(module_path, metadata["command_line_args"])
    metadata["module_name"] = module.name
    metadata["version"] = module.version
    metadata["semantic_version"] = str(version_to_semantic_version(module.version))
    metadata["commands"] = [cmd.to_dict() for cmd in module.commands if cmd.command_name not in metadata["exclude_commands"]]
    
    # overide requested commands data
    for overide in metadata["overide_command"]:
        if 'command_name' not in overide:
            print("error: the given overide json does not contains command name: %s" % str(overide))
            continue
        overide_index = [i for i in range(len(metadata["commands"])) if metadata["commands"][i]['command_name'] == overide['command_name']]
        if len(overide_index) != 1:
            print("error: the given overide command appears more then once")
            continue
        if verbose:
            print('overiding %s with %s' % (str(metadata["commands"][overide_index[0]]), str(overide)))
        metadata["commands"][overide_index[0]] = overide

    if module_name:
        metadata["module_name"] = module_name
        
    try:
        p = Popen('git rev-parse HEAD'.split(' '), stdin=PIPE, stdout=PIPE, stderr=PIPE)
        git_sha, err = p.communicate()
        if err != '':
            print("could not extract git sha %s" % err)
        else:
            metadata["git_sha"] = git_sha.strip()
    except Exception:
        print("could not extract git sha %s" % err)

    if print_filename_only:
        # For scripts, it might be helpful to know the formatted filename
        # ahead of time, so that it can manipulate it later on.
        print(output.format(**metadata))
        return 0

    if verbose:
        print("Module Metadata:")
        print(json.dumps(metadata, indent=2))

    archive(module_path, metadata, archive_name=output)
    return 0
