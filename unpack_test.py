import os
import hashlib

from RAMP import packer, unpacker, module_metadata

MODULE_FILE = "redisgraph.so"
MODULE_FILE_PATH = os.path.join(os.getcwd() + "/test_module", MODULE_FILE)
BUNDLE_ZIP_FILE = "module.zip"


def sha256_checksum(filename, block_size=65536):
    """Computes sha256 for given file"""
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()


def test_bad_bundle():
    """
    test malformed bundle is detected
    """
    pass


def test_valid_bundle():
    """
    test bundle extraction
    """
    module_path = os.path.join(os.getcwd(), MODULE_FILE_PATH)
    path_to_bundle = os.path.join(os.getcwd(), BUNDLE_ZIP_FILE)
    metadata = module_metadata.create_default_metadata(module_path)
    metadata['module_name'] = 'module_name'

    packer.archive(module_path, metadata)
    metadata, binary, files = unpacker.unpack(path_to_bundle)
    assert metadata is not None
    assert binary is not None
    assert files is None


if __name__ == '__main__':
    test_bad_bundle()
    test_valid_bundle()
