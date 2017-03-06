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
EXTRA_FILES = []
COMMAND_LINE_ARGS = ""
MIN_REDIS_VERSION = 4.0

FIELDS = ["Module_name", "Module_file", "Architecture", "Version", "Author", "Email",
          "Description", "Homepage", "License", "Extra_files", "Command_line_args",
          "Min_redis_version", "SHA256", "Commands"]

def sha256_checksum(filename, block_size=65536):
    """Computes sha256 for given file"""
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()

def create_default_metadata(module, module_path):
    """Creates a default metadata"""
    metadata = {
        "Module_name" : module.name,
        "Module_file" : os.path.basename(module_path),
        "Architecture" : ARCHITECTURE,
        "Version" : module.version,
        "Author" : AUTHOR,
        "Email" : EMAIL,
        "Description" : DESCRIPTION,
        "Homepage" : HOMEPAGE,
        "License" : LICENSE,
        "Extra_files" : EXTRA_FILES,
        "Command_line_args" : COMMAND_LINE_ARGS,
        "Min_redis_version" : MIN_REDIS_VERSION,
        "SHA256" : sha256_checksum(module_path),
        "Commands": [cmd.to_dict() for cmd in module.commands]
    }
    return metadata
