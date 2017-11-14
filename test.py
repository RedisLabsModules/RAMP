import os
import yaml
from RAMP import packer, module_metadata
import click
import hashlib
from click.testing import CliRunner
import module_unpacker
from module_capabilities import MODULE_CAPABILITIES

MODULE_FILE = "redisgraph.so"
MODULE_VERSION = 30201
MODULE_SEMANTIC_VERSION = "3.2.1"
MENIFEST_FILE = "example.manifest.yml"
MODULE_FILE_PATH = os.path.join(os.getcwd() + "/test_module", MODULE_FILE)
MENIFEST_FILE_PATH = os.path.join(os.getcwd(), MENIFEST_FILE)
BUNDLE_ZIP_FILE = "test_module.zip"

def sha256_checksum(filename, block_size=65536):
    """Computes sha256 for given file"""
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()


def validate_module_commands(commands):
    assert len(commands) == 3

    # Expected commands:
    graph_explain = {"command_arity": -1,
                         "command_name": "graph.EXPLAIN",
                         "first_key": 1,
                         "flags": ["write"],
                         "last_key": 1,
                         "step": 1}
    assert commands[0] == graph_explain

    graph_query = {"command_arity": -1,
                   "command_name": "graph.QUERY",
                   "first_key": 1,
                   "flags": ["write"],
                   "last_key": 1,
                   "step": 1}
    assert commands[1] == graph_query

    graph_delete = {"command_arity": -1,
                    "command_name": "graph.DELETE",
                    "first_key": 1,
                    "flags": ["write"],
                    "last_key": 1,
                    "step": 1}
    assert commands[2] == graph_delete

def test_defaults():
    """Test auto generated metadata from module is as expected."""
    runner = CliRunner()
    result = runner.invoke(packer.package, [MODULE_FILE_PATH, '-o', BUNDLE_ZIP_FILE])
    assert result.exit_code == 0

    metadata, _ = module_unpacker.unpack(BUNDLE_ZIP_FILE)
    assert metadata["module_name"] == "graph"
    assert metadata["module_file"] == MODULE_FILE
    assert metadata["architecture"] == 'x86_64'
    assert metadata["version"] == MODULE_VERSION
    assert metadata["semantic_version"] == MODULE_SEMANTIC_VERSION
    assert metadata["display_name"] == module_metadata.DISPLAY_NAME
    assert metadata["author"] == module_metadata.AUTHOR
    assert metadata["email"] == module_metadata.EMAIL
    assert metadata["description"] == module_metadata.DESCRIPTION
    assert metadata["homepage"] == module_metadata.HOMEPAGE
    assert metadata["license"] == module_metadata.LICENSE
    assert metadata["command_line_args"] == module_metadata.COMMAND_LINE_ARGS
    assert metadata["min_redis_version"] == module_metadata.MIN_REDIS_VERSION
    assert metadata["min_redis_pack_version"] == module_metadata.MIN_REDIS_PACK_VERSION
    assert metadata["capabilities"] == module_metadata.MODULE_CAPABILITIES
    assert metadata["ramp_format_version"] == module_metadata.RAMP_FORMAT_VERSION
    assert metadata["sha256"] == sha256_checksum(MODULE_FILE_PATH)
    validate_module_commands(metadata["commands"])

def test_bundle_from_cmd():
    """
    Test metadata generated from command line arguments is as expected.
    """

    author = "redislabs"
    email = "roi@redislabs.com"
    description = "desc some module"
    homepage = "http://github.com/redismodules/module"
    _license = "AGPL"
    command_line_args = "\"-output f --level debug\""
    min_redis_version = "4.6"
    min_redis_pack_version = "5.0"
    display_name = "test_module"

    argv = [MODULE_FILE_PATH, '-a', author, '-e', email, '-D', description, '-d', display_name,
            '-h', homepage, '-l', _license, '-c', command_line_args, '-r', min_redis_version,
            '-R', min_redis_pack_version, '-C', ','.join([cap['name'] for cap in MODULE_CAPABILITIES]), '-o', BUNDLE_ZIP_FILE]

    runner = CliRunner()
    result = runner.invoke(packer.package, argv)

    assert result.exit_code == 0
    metadata, _ = module_unpacker.unpack(BUNDLE_ZIP_FILE)

    assert metadata["module_name"] == "graph"
    assert metadata["module_file"] == MODULE_FILE
    assert metadata["architecture"] == "x86_64"
    assert metadata["display_name"] == display_name
    assert metadata["version"] == MODULE_VERSION
    assert metadata["semantic_version"] == MODULE_SEMANTIC_VERSION
    assert metadata["author"] == author
    assert metadata["email"] == email
    assert metadata["description"] == description
    assert metadata["homepage"] == homepage
    assert metadata["license"] == _license
    assert metadata["command_line_args"] == command_line_args
    assert metadata["min_redis_version"] == min_redis_version
    assert metadata["min_redis_pack_version"] == min_redis_pack_version
    assert metadata["sha256"] == sha256_checksum(MODULE_FILE_PATH)
    assert len(metadata["capabilities"]) == len(MODULE_CAPABILITIES)

    commands = metadata["commands"]
    validate_module_commands(commands)

def test_bundle_from_menifest():
    """
    Test metadata generated from menifest file is as expected.
    """

    runner = CliRunner()
    result = runner.invoke(packer.package, [MODULE_FILE_PATH, '-m', MENIFEST_FILE_PATH, '-o', BUNDLE_ZIP_FILE])

    assert result.exit_code == 0
    metadata, _ = module_unpacker.unpack(BUNDLE_ZIP_FILE)

    assert metadata["module_name"] == "graph"
    assert metadata["module_file"] == MODULE_FILE
    assert metadata["architecture"] == "x86_64"
    assert metadata["version"] == MODULE_VERSION
    assert metadata["semantic_version"] == MODULE_SEMANTIC_VERSION
    assert metadata["sha256"] == sha256_checksum(MODULE_FILE_PATH)

    with open(MENIFEST_FILE_PATH, 'r') as f:
        manifest = yaml.load(f)
        for key in manifest:
            assert metadata[key] == manifest[key]

    commands = metadata["commands"]
    validate_module_commands(commands)

if __name__ == '__main__':
    test_defaults()
    test_bundle_from_menifest()
    test_bundle_from_cmd()
    print "PASS"
