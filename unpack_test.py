import os
import hashlib
import unittest
import module_packer
import module_unpacker
import module_metadata
from commands_discovery import discover_modules_commands

MODULE_FILE = "libmodule.so"
MODULE_FILE_PATH = os.path.join(os.getcwd() + "/test_module", MODULE_FILE)
print "MODULE_FILE_PATH %s" % MODULE_FILE_PATH
BUNDLE_ZIP_FILE = "module.zip"

def sha256_checksum(filename, block_size=65536):
    """Computes sha256 for given file"""
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()

class TestModuleUnpacker(unittest.TestCase):
    def test_bad_bundle(self):
        """
        test malformed bundle is detected
        """
        path_to_bundle = os.path.join(os.getcwd(), BUNDLE_ZIP_FILE)

        module = discover_modules_commands(MODULE_FILE_PATH)
        metadata = module_metadata.create_default_metadata(module, MODULE_FILE_PATH)

        fields = ["Module_name", "Architecture", "Version", "SHA256"]
        for field in fields:
            tmp = metadata[field]
            metadata[field] = ""
            module_packer.archive(MODULE_FILE_PATH, metadata)
            self.assertIsNone(module_unpacker.unpack(path_to_bundle))
            metadata[field] = tmp
            os.remove(path_to_bundle)

    def test_valid_bundle(self):
        """
        test bundle extraction
        """
        module_path = os.path.join(os.getcwd(), MODULE_FILE)
        path_to_bundle = os.path.join(os.getcwd(), BUNDLE_ZIP_FILE)
        path_to_metadata = os.path.join(os.getcwd(), "module.json")
        module = discover_modules_commands(module_path)
        metadata = module_metadata.create_default_metadata(module, module_path)

        module_packer.archive(module_path, metadata)
        metadata, path_to_module = module_unpacker.unpack(path_to_bundle)
        self.assertIsNotNone(metadata)

        self.assertTrue(os.path.isfile(path_to_module))
        self.assertTrue(os.path.isfile(path_to_metadata))

        os.remove(path_to_bundle)
        os.remove(path_to_metadata)
        os.remove(module_path)

if __name__ == '__main__':
    unittest.main()
