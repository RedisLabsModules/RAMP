import os
import hashlib
import platform

# Defaults
ARCHITECTURE = platform.machine()
OS = platform.system()
DISPLAY_NAME = ""
AUTHOR = ""
EMAIL = ""
DESCRIPTION = ""
HOMEPAGE = ""
LICENSE = ""
MODULE_NAME = ""
MODULE_VERSION = 1
MODULE_SEMANTIC_VERSION = '0.0.1'
MODULE_COMMANDS = []
EXCLUDE_COMMANDS = []
MODULE_CAPABILITIES = []
COMMAND_LINE_ARGS = ""
MIN_REDIS_VERSION = "4.0"
MIN_REDIS_PACK_VERSION = "5.0"
RAMP_FORMAT_VERSION = 1
CONFIG_COMMAND = ""
OVERIDE_COMMAND = []

FIELDS = [
    "architecture",
    "author",
    "capabilities",
    "command_line_args",
    "commands",
    "config_command",
    "description",
    "display_name",
    "email",
    "exclude_commands",
    "git_sha",
    "homepage",
    "license",
    "min_redis_pack_version",
    "min_redis_version",
    "module_file",
    "module_name",
    "os",
    "overide_command",
    "ramp_format_version",
    "semantic_version",
    "sha256",
    "version",
]

def sha256_checksum(filename, block_size=65536):
    """Computes sha256 for given file"""
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()

def create_default_metadata(module_path):
    """Creates a default metadata"""
    metadata = {
        "module_name" : MODULE_NAME,
        "module_file": os.path.basename(module_path),
        "os": OS,
        "architecture": ARCHITECTURE,
        "version": MODULE_VERSION,
        "semantic_version": MODULE_SEMANTIC_VERSION,
        "display_name": DISPLAY_NAME,
        "author": AUTHOR,
        "email": EMAIL,
        "description": DESCRIPTION,
        "homepage": HOMEPAGE,
        "license": LICENSE,
        "command_line_args": COMMAND_LINE_ARGS,
        "capabilities": MODULE_CAPABILITIES,
        "min_redis_version": MIN_REDIS_VERSION,
        "min_redis_pack_version": MIN_REDIS_PACK_VERSION,
        "sha256": sha256_checksum(module_path),
        "commands": MODULE_COMMANDS,
        "ramp_format_version": RAMP_FORMAT_VERSION,
        "config_command": CONFIG_COMMAND,
        "exclude_commands": EXCLUDE_COMMANDS,
        "overide_command": OVERIDE_COMMAND
    }
    return metadata
