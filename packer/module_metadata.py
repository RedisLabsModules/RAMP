import os
import hashlib

# Defaults
ARCHITECTURE = 64
VERSION = "1.0"
AUTHOR = ""
EMAIL = ""
DESCRIPTION = ""
HOMEPAGE = ""
LICENSE = ""
MODULE_NAME = ""
MODULE_VERSION = "1.0"
MODULE_COMMANDS = []
EXTRA_FILES = []
COMMAND_LINE_ARGS = ""
MIN_REDIS_VERSION = "4.0"
MIN_RLEC_VERSION = "5.2"

FIELDS = ["module_name", "module_file", "architecture", "version", "author", "email",
          "description", "homepage", "license", "extra_files", "command_line_args",
          "min_redis_version", "min_rlec_version", "sha256", "commands"]

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
        "architecture": ARCHITECTURE,
        "version": MODULE_VERSION,
        "author": AUTHOR,
        "email": EMAIL,
        "description": DESCRIPTION,
        "homepage": HOMEPAGE,
        "license": LICENSE,
        "extra_files": EXTRA_FILES,
        "command_line_args": COMMAND_LINE_ARGS,
        "min_redis_version": MIN_REDIS_VERSION,
        "min_rlec_version": MIN_RLEC_VERSION,
        "sha256": sha256_checksum(module_path),
        "commands": MODULE_COMMANDS
    }
    return metadata
