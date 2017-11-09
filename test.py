import os
import yaml
from RAMP import packer
import click
import hashlib
from click.testing import CliRunner
import module_unpacker
from module_capabilities import MODULE_CAPABILITIES
from RAMP.module_metadata import MODULE_VERSION

MODULE_FILE = "redisgraph.so"
MENIFEST_FILE = "example.manifest.yml"
MODULE_FILE_PATH = os.path.join(os.getcwd() + "/test_module", MODULE_FILE)
MENIFEST_FILE_PATH = os.path.join(os.getcwd(), MENIFEST_FILE)
BUNDLE_ZIP_FILE = "module.zip"

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
    result = runner.invoke(packer.package, [MODULE_FILE_PATH])
    assert result.exit_code == 0

    metadata, _ = module_unpacker.unpack('./module.zip')

    assert metadata["module_name"] == "graph"
    assert metadata["module_file"] == MODULE_FILE
    assert metadata["architecture"] == 'x86_64'
    assert metadata["version"] == MODULE_VERSION
    assert metadata["author"] == ""
    assert metadata["email"] == ""
    assert metadata["description"] == ""
    assert metadata["homepage"] == ""
    assert metadata["license"] == ""
    assert metadata["command_line_args"] == ""
    assert metadata["min_redis_version"] == "4.0"
    assert metadata["min_redis_pack_version"] == "5.0"
    assert metadata["capabilities"] == []
    assert metadata["sha256"] == sha256_checksum(MODULE_FILE_PATH)
    validate_module_commands(metadata["commands"])

def test_bundle_from_cmd():
    """
    Test metadata generated from command line arguments is as expected.
    """

    author = "redislabs"
    email = "r@redislabs.com"
    description = "desc some module"
    homepage = "http://github.com/redismodules/module"
    _license = "AGPL"
    command_line_args = "\"-output f --level debug\""
    min_redis_version = "4.6"
    min_redis_pack_version = "5.0"

    argv = [MODULE_FILE_PATH, '-a', author, '-e', email, '-d', description,
            '-h', homepage, '-l', _license, '-c', command_line_args, '-r', min_redis_version,
            '-rl', min_redis_pack_version, '-ca', ','.join([cap['name'] for cap in MODULE_CAPABILITIES])]

    runner = CliRunner()
    result = runner.invoke(packer.package, argv)

    assert result.exit_code == 0
    metadata, _ = module_unpacker.unpack('./module.zip')

    assert metadata["module_name"] == "graph"
    assert metadata["module_file"] == MODULE_FILE
    assert metadata["architecture"] == "x86_64"
    assert metadata["version"] == MODULE_VERSION
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
    result = runner.invoke(packer.package, [MODULE_FILE_PATH, '-m', MENIFEST_FILE_PATH])

    assert result.exit_code == 0
    metadata, _ = module_unpacker.unpack('./module.zip')

    assert metadata["module_name"] == "graph"
    assert metadata["module_file"] == MODULE_FILE
    assert metadata["architecture"] == "x86_64"
    assert metadata["version"] == MODULE_VERSION
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
