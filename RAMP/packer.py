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
    metadata = set_defaults(module_path)

    manifest = args['manifest']
    if manifest:
        init_from_manifest(metadata, manifest)

    nonkeys = dict.fromkeys(['manifest', 'verbose', 'print_filename_only', 'output', 'override_command'], 1)
    for key, value in args.iteritems():
        if key in nonkeys or key not in module_metadata.FIELDS:
            continue
        if value is None or value == []:
            continue
        metadata[key] = value

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

    module_name = args['module_name']
    if module_name:
        metadata["module_name"] = module_name

    try:
        p = Popen('git rev-parse HEAD'.split(' '), stdin=PIPE, stdout=PIPE, stderr=PIPE)
        git_sha, err = p.communicate()
        if p.returncode != 0:
            print("could not extract git sha {}".format(err))
        else:
            metadata["git_sha"] = git_sha.strip()
    except Exception:
        print("could not extract git sha {}".format(err))

    output = args['output']
    if args['print_filename_only']:
        # For scripts, it might be helpful to know the formatted filename
        # ahead of time, so that it can manipulate it later on.
        print(output.format(**metadata))
        return 0

    if args['verbose']:
        print("Module Metadata:")
        print(json.dumps(metadata, indent=2))

    archive(module_path, metadata, archive_name=output)
    return 0
