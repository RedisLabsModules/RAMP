import os
import yaml
import click
import hashlib
from click.testing import CliRunner

from module_capabilities import MODULE_CAPABILITIES
from RAMP import ramp, packer, unpacker, module_metadata


MODULE_FILE = "redisgraph.so"
MODULE_VERSION = 10012
MODULE_SEMANTIC_VERSION = "1.0.12"
MENIFEST_FILE = "example.manifest.yml"
MENIFEST2_FILE = "example2.manifest.yml"
MODULE_FILE_PATH = os.path.join(os.getcwd() + "/test_module", MODULE_FILE)
MENIFEST_FILE_PATH = os.path.join(os.getcwd(), MENIFEST_FILE)
MENIFEST2_FILE_PATH = os.path.join(os.getcwd(), MENIFEST2_FILE)
BUNDLE_ZIP_FILE = "test_module.zip"
CONFIG_COMMAND = "MODULE.CONFIG"

def sha256_checksum(filename, block_size=65536):
    """Computes sha256 for given file"""
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()

def get_git_sha():
    try:
        p = Popen('git rev-parse HEAD'.split(' '), stdin=PIPE, stdout=PIPE, stderr=PIPE)
        git_sha, err = p.communicate()
        if err != '':
            return None
        else:
            return git_sha.strip()
    except Exception:
        return None


def validate_module_commands(commands):
    assert len(commands) == 4

    # Expected commands:
    expected_command = []
    expected_command.append({"command_name": "graph.EXPLAIN"})

    expected_command.append({"command_arity": -1,
                   "command_name": "graph.QUERY",
                   "first_key": 1,
                   "flags": ["write", "denyoom", "module", "noscript"],
                   "last_key": 1,
                   "step": 1})

    expected_command.append({"command_arity": -1,
                    "command_name": "graph.DELETE",
                    "first_key": 1,
                    "flags": ["write","module","noscript"],
                    "last_key": 1,
                    "step": 1})

    expected_command.append({"command_name": "test"})

    expected_set = sorted(expected_command, key=lambda c: c['command_name'])
    actual_set = sorted(commands, key=lambda c: c['command_name'])
    assert expected_set == actual_set

def test_defaults():
    """Test auto generated metadata from module is as expected."""
    runner = CliRunner()
    result = runner.invoke(ramp.pack, [MODULE_FILE_PATH, '-o', BUNDLE_ZIP_FILE,
                                       '-E', 'graph.BULK',
                                       '--overide-command', '{"command_name": "graph.EXPLAIN"}',
                                       '--add-command', '{"command_name": "test"}'])
    assert result.exit_code == 0

    metadata = unpacker.unpack(BUNDLE_ZIP_FILE)[0]
    assert metadata["module_name"] == "graph"
    assert metadata["module_file"] == MODULE_FILE
    assert metadata["architecture"] == 'x86_64'
    assert metadata["version"] == MODULE_VERSION
    assert metadata["semantic_version"] == MODULE_SEMANTIC_VERSION
    assert metadata["display_name"] == module_metadata.DISPLAY_NAME
    assert metadata["capability_name"] == module_metadata.CAPABILITY_NAME
    assert metadata["author"] == module_metadata.AUTHOR
    assert metadata["email"] == module_metadata.EMAIL
    assert metadata["description"] == module_metadata.DESCRIPTION
    assert metadata["homepage"] == module_metadata.HOMEPAGE
    assert metadata["license"] == module_metadata.LICENSE
    assert metadata["command_line_args"] == module_metadata.COMMAND_LINE_ARGS
    assert metadata["min_redis_version"] == module_metadata.MIN_REDIS_VERSION
    assert metadata["min_redis_pack_version"] == module_metadata.MIN_REDIS_PACK_VERSION
    assert metadata["config_command"] == module_metadata.CONFIG_COMMAND
    assert metadata["capabilities"] == module_metadata.MODULE_CAPABILITIES
    assert metadata["ramp_format_version"] == module_metadata.RAMP_FORMAT_VERSION
    assert metadata["sha256"] == sha256_checksum(MODULE_FILE_PATH)
    assert 'redis_args' not in metadata

    git_sha = get_git_sha()
    if git_sha is not None:
        assert metadata["git_sha"] == git_sha

    validate_module_commands(metadata["commands"])

def test_bundle_from_cmd():
    """
    Test metadata generated from command line arguments is as expected.
    """

    author = "redis"
    email = "roi@redis.com"
    description = "desc some module"
    homepage = "http://github.com/redismodules/module"
    _license = "AGPL"
    command_line_args = "\\\"-output f --level debug\\\""
    min_redis_version = "4.6"
    min_redis_pack_version = "5.0"
    compatible_redis_version = "7.2"
    bigstore_version_2_support = True
    display_name = "test_module"
    capability_name = "Test & Module"
    module_name = "module_test"

    argv = [MODULE_FILE_PATH, '-a', author, '-e', email, '-D', description,
            '-d', display_name, '-b', capability_name, '-n', module_name,
            '-h', homepage, '-l', _license, '-c', command_line_args,
            '-r', min_redis_version, '-R', min_redis_pack_version, '-cr', compatible_redis_version,
            '--bigstore-version-2-support',
            '-C', ','.join([cap['name'] for cap in MODULE_CAPABILITIES]),
            '-o', BUNDLE_ZIP_FILE, '-cc', CONFIG_COMMAND, '-E', 'graph.bulk',
            '-E', 'graph.BULK',
            '--overide-command', '{"command_name": "graph.EXPLAIN"}',
            '--add-command', '{"command_name": "test"}',
            '--redis-args', '{"loglevel": "debug"}']

    runner = CliRunner()
    result = runner.invoke(ramp.pack, argv)

    assert result.exit_code == 0
    metadata = unpacker.unpack(BUNDLE_ZIP_FILE)[0]

    assert metadata["module_name"] == module_name
    assert metadata["module_file"] == MODULE_FILE
    assert metadata["architecture"] == "x86_64"
    assert metadata["display_name"] == display_name
    assert metadata["capability_name"] == capability_name
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
    assert metadata["compatible_redis_version"] == compatible_redis_version
    assert metadata["bigstore_version_2_support"] == bigstore_version_2_support
    assert metadata["config_command"] == CONFIG_COMMAND
    assert metadata["sha256"] == sha256_checksum(MODULE_FILE_PATH)
    assert len(metadata["capabilities"]) == len(MODULE_CAPABILITIES)
    assert 'redis_args' not in metadata

    git_sha = get_git_sha()
    if git_sha is not None:
        assert metadata["git_sha"] == git_sha

    commands = metadata["commands"]
    validate_module_commands(commands)

def _test_bundle_from_manifest(manifest_file, manifest_file_path):
    """
    Test metadata generated from menifest file is as expected.
    """

    runner = CliRunner()
    result = runner.invoke(ramp.pack, [MODULE_FILE_PATH, '-m', manifest_file_path, '-o', BUNDLE_ZIP_FILE])

    assert result.exit_code == 0
    metadata = unpacker.unpack(BUNDLE_ZIP_FILE)[0]

    assert metadata["module_name"] == "graph"
    assert metadata["module_file"] == MODULE_FILE
    assert metadata["architecture"] == "x86_64"
    assert metadata["version"] == MODULE_VERSION
    assert metadata["semantic_version"] == MODULE_SEMANTIC_VERSION
    assert metadata["sha256"] == sha256_checksum(MODULE_FILE_PATH)
    assert metadata["config_command"] == CONFIG_COMMAND
    assert metadata["crdb"] == {"supported_featureset_versions": [1, 3]}

    git_sha = get_git_sha()
    if git_sha is not None:
        assert metadata["git_sha"] == git_sha

    with open(MENIFEST_FILE_PATH, 'r') as f:
        manifest = yaml.load(f, Loader=yaml.FullLoader)
        for key in manifest:
            if key == 'dependencies' or key == 'optional-dependencies':
                assert metadata[key] == unpacker.normalize_dependencies(manifest[key])
            elif key == 'redis_args':
                assert 'redis_args' not in metadata
            else:
                assert metadata[key] == manifest[key]

    commands = metadata["commands"]
    validate_module_commands(commands)

def test_bundle_from_manifest():
    _test_bundle_from_manifest(MENIFEST_FILE, MENIFEST_FILE_PATH)

def test_bundle_from_menifest2():
    _test_bundle_from_manifest(MENIFEST2_FILE, MENIFEST2_FILE_PATH)

def test_cli_unpack():
    """Test CLI unpack command correctly extracts binary files."""
    import tempfile
    
    # Use existing test bundle if available, otherwise skip
    bundle_path = os.path.join(os.getcwd(), "test_assets", 
                              "redisgears_python.Linux-ubuntu18.04-x86_64.1.2.5.zip")
    
    if not os.path.exists(bundle_path):
        print("⚠️  CLI unpack test skipped: test bundle not found")
        return
    
    # Create temporary directory for extraction
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        
        try:
            # Change to temp directory for extraction
            os.chdir(temp_dir)
            
            # Test CLI unpack command
            runner = CliRunner()
            result = runner.invoke(ramp.unpack, [bundle_path])
            
            # Verify command succeeded
            assert result.exit_code == 0, (
                f"CLI unpack failed with exit code {result.exit_code}\n"
                f"Output: {result.output}\n"
                f"Exception: {result.exception}"
            )
            
            # Check that binary file was extracted correctly
            extracted_files = os.listdir('.')
            so_files = [f for f in extracted_files if f.endswith('.so')]
            assert len(so_files) > 0, f"No .so binary file extracted. Files: {extracted_files}"
            
            # Verify binary file is valid ELF
            so_file = so_files[0]
            with open(so_file, 'rb') as f:
                header = f.read(4)
                assert header == b'\x7fELF', f"Binary file corrupted: expected ELF header, got {header.hex()}"
            
        finally:
            os.chdir(original_cwd)

if __name__ == '__main__':
    test_defaults()
    test_bundle_from_manifest()
    test_bundle_from_cmd()
    test_cli_unpack()
    print("PASS")
