import os
import hashlib
import platform
from typing import List, Dict, Any  # noqa: F401
from .common import *


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
MODULE_VERSION = "1.0"
MODULE_SEMANTIC_VERSION = '0.0.1'
MODULE_COMMANDS = []  # type: List[Dict[str, str]]
EXCLUDE_COMMANDS = []  # type: List[str]
MODULE_CAPABILITIES = []  # type: List[Dict[str, str]]
MODULE_DEPENDENCIES = []  # type: Dict[str, Dict[str, str]]
MODULE_OPTIONAL_DEPENDENCIES = []  # type: Dict[str, Dict[str, str]]
COMMAND_LINE_ARGS = ""
RUN_COMMAND_LINE_ARGS = None
MIN_REDIS_VERSION = "4.0"
MIN_REDIS_PACK_VERSION = "5.2"
RAMP_FORMAT_VERSION = 1
CONFIG_COMMAND = ""
OVERIDE_COMMAND = []  # type: List[Dict[str, str]]
ADD_COMMAND = []  # type: List[Dict[str, str]]
CRDB_ARGS = {}  # type: List[Dict[str, str]]

FIELDS = [
    "architecture",
    "author",
    "capabilities",
    "command_line_args",
    "run_command_line_args",
    "commands",
    "config_command",
    "dependencies",
    "optional-dependencies",
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
    "add_command",
    "ramp_format_version",
    "semantic_version",
    "sha256",
    "version",
    "crdb"
]  # type: List[str]


def sha256_checksum(filename, block_size=65536):
    # type: (str, int) -> str
    """Computes sha256 for given file"""
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()


def create_default_metadata(module_path):
    # type: (str) -> Dict[str, Any]
    """Creates a default metadata"""
    return {
        "module_name": MODULE_NAME,
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
        "run_command_line_args": RUN_COMMAND_LINE_ARGS,
        "capabilities": MODULE_CAPABILITIES,
        "dependencies": MODULE_DEPENDENCIES,
        "optional-dependencies": MODULE_OPTIONAL_DEPENDENCIES,
        "min_redis_version": MIN_REDIS_VERSION,
        "min_redis_pack_version": MIN_REDIS_PACK_VERSION,
        "sha256": sha256_checksum(module_path),
        "commands": MODULE_COMMANDS,
        "ramp_format_version": RAMP_FORMAT_VERSION,
        "config_command": CONFIG_COMMAND,
        "exclude_commands": EXCLUDE_COMMANDS,
        "overide_command": OVERIDE_COMMAND,
        "add_command": ADD_COMMAND,
        "crdb": CRDB_ARGS,
    }
