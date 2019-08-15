import os
import json
import zipfile
import yaml
import semantic_version
import tempfile
from subprocess import Popen, PIPE

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

def init_from_manifest(metadata, manifest):
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
    with tempfile.NamedTemporaryFile(mode='w', prefix='ramp.json', delete=False) as outfile:
        jfile = outfile.name
        archive_name = archive_name.format(**metadata)
        json.dump(metadata, outfile, indent=4, sort_keys=True)

    try:
        with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as archive_file:
            archive_file.write(module_path, metadata["module_file"])
            archive_file.write(jfile, arcname='module.json')
            print(archive_name)
    finally:
        os.remove(jfile)


def package(module, **args):
    module_path = module

    nonkeys = dict.fromkeys(['manifest', 'verbose', 'print_filename_only', 'output'], 1)
    manifest = args['manifest']
    verbose = args['verbose']
    print_filename_only = args['print_filename_only']
    output = args['output']

    # start with default values (lowest priority)
    metadata = set_defaults(module_path)

    # fill in keys from manifest file
    if manifest:
        init_from_manifest(metadata, manifest)

    # fill in keys from arguments
    for key in args.keys():
        if key in nonkeys:
            continue
        value = args[key]
        if value is None or value == []:
            continue
        metadata[key] = value

    # Load module into redis and discover its commands
    module = discover_modules_commands(module_path, metadata["command_line_args"])
    metadata["module_name"] = module.name
    metadata["version"] = module.version
    metadata["semantic_version"] = str(version_to_semantic_version(module.version))
    metadata["commands"] = [cmd.to_dict() for cmd in module.commands if cmd.command_name not in metadata["exclude_commands"]]

    # fill in keys from arguments once more (highest prioriry)
    for key in args.keys():
        if key in nonkeys:
            continue
        value = args[key]
        if value is None or value == []:
            continue
        metadata[key] = value

    # override requested commands data
    for override in metadata["overide_command"]:
        if 'command_name' not in override:
            print("error: the given override json does not contains command name: %s" % str(override))
            continue
        override_index = [i for i in range(len(metadata["commands"])) if metadata["commands"][i]['command_name'] == override['command_name']]
        if len(override_index) != 1:
            print("error: the given override command appears more then once")
            continue
        if verbose:
            print('overiding %s with %s' % (str(metadata["commands"][override_index[0]]), str(override)))
        metadata["commands"][override_index[0]] = override

    module_name = args['module_name']
    if module_name:
        metadata["module_name"] = module_name

    try:
        p = Popen('git rev-parse HEAD'.split(' '), stdin=PIPE, stdout=PIPE, stderr=PIPE)
        git_sha, err = p.communicate()
        if p.returncode != 0:
            print("could not extract git sha {}".format(err))
        else:
            metadata["git_sha"] = str(git_sha.strip())
    except Exception:
        print("could not extract git sha {}".format(err))

    # cleanup metadata from utility keys
    fields = dict.fromkeys(module_metadata.FIELDS, 1)
    for key in metadata.keys():
        if not key in fields:
            metadata.pop(key)

    if print_filename_only:
        # For scripts, it might be helpful to know the formatted filename
        # ahead of time, so that it can manipulate it later on.
        print(output.format(**metadata))
        return 0

    if args['verbose']:
        print("Module Metadata:")
        print(json.dumps(metadata, indent=2))

    archive(module_path, metadata, archive_name=output)
    return 0
