import os
import hashlib
import platform
# Defaults
ARCHITECTURE = platform.machine()
OS = platform.system()
VERSION = "1.0"
DISPLAY_NAME = ""
AUTHOR = ""
EMAIL = ""
DESCRIPTION = ""
HOMEPAGE = ""
LICENSE = ""
MODULE_NAME = ""
MODULE_VERSION = "1.0"
MODULE_COMMANDS = []
MODULE_CAPABILITIES = []
COMMAND_LINE_ARGS = ""
MIN_REDIS_VERSION = "4.0"
MIN_RLEC_VERSION = "5.2"

FIELDS = ["module_name", "module_file", "architecture", "version", "display_name", "author", "email",
          "description", "homepage", "license", "command_line_args", "capabilities",
          "min_redis_version", "min_rlec_version", "sha256", "commands", "os"]

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
        "display_name": DISPLAY_NAME,
        "author": AUTHOR,
        "email": EMAIL,
        "description": DESCRIPTION,
        "homepage": HOMEPAGE,
        "license": LICENSE,
        "command_line_args": COMMAND_LINE_ARGS,
        "capabilities": MODULE_CAPABILITIES,
        "min_redis_version": MIN_REDIS_VERSION,
        "min_rlec_version": MIN_RLEC_VERSION,
        "sha256": sha256_checksum(module_path),
        "commands": MODULE_COMMANDS
    }
    return metadata
