import os
import hashlib
import unittest
import module_packer
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

class TestModulePacker(unittest.TestCase):
    def validate_module_commands(self, commands):
        self.assertEqual(len(commands), 4)

        # Expected commands:
        graph_remove_edge = {"command_arity": -1,
                             "command_name": "graph.REMOVEEDGE",
                             "first_key": 1,
                             "flags": ["write"],
                             "last_key": 1,
                             "step": 1}
        self.assertEqual(commands[0], graph_remove_edge)

        graph_query = {"command_arity": -1,
                       "command_name": "graph.QUERY",
                       "first_key": 1,
                       "flags": ["write"],
                       "last_key": 1,
                       "step": 1}
        self.assertEqual(commands[1], graph_query)

        graph_add_edge = {"command_arity": -1,
                          "command_name": "graph.ADDEDGE",
                          "first_key": 1,
                          "flags": ["write"],
                          "last_key": 1,
                          "step": 1}
        self.assertEqual(commands[2], graph_add_edge)

        graph_delete = {"command_arity": -1,
                        "command_name": "graph.DELETE",
                        "first_key": 1,
                        "flags": ["write"],
                        "last_key": 1,
                        "step": 1}
        self.assertEqual(commands[3], graph_delete)

    def test_defaults(self):
        """Test auto generated metadata from module is as expected."""
        metadata = module_packer.set_defaults(MODULE_FILE_PATH)

        self.assertEqual(metadata["module_name"], "")
        self.assertEqual(metadata["module_file"], MODULE_FILE)
        self.assertEqual(metadata["architecture"], 64)
        self.assertEqual(metadata["version"], "1.0")
        self.assertEqual(metadata["author"], "")
        self.assertEqual(metadata["email"], "")
        self.assertEqual(metadata["description"], "")
        self.assertEqual(metadata["homepage"], "")
        self.assertEqual(metadata["license"], "")
        self.assertEqual(metadata["extra_files"], [])
        self.assertEqual(metadata["command_line_args"], "")
        self.assertEqual(metadata["min_redis_version"], "4.0")
        self.assertEqual(metadata["min_rlec_version"], "5.2")
        self.assertEqual(metadata["sha256"], sha256_checksum(MODULE_FILE_PATH))

        commands = metadata["commands"]
        # TODO: test to additional unexcpected fields.
        # self.validate_module_commands(commands)

    def test_bundle_from_cmd(self):
        """
        Test metadata generated from command line arguments is as expected.
        """

        architecture = "64"
        author = "redislabs"
        email = "r@redislabs.com"
        description = "desc some module"
        homepage = "http://github.com/redismodules/module"
        _license = "AGPL"
        extra_files = []
        command_line_args = "-output f --level debug"
        min_redis_version = "4.6"
        min_rlec_version = "5.2"

        argv = ['-a', author, '-e', email, '-ar', architecture, '-d', description,
                '-ho', homepage, '-l', _license, '-c', command_line_args, '-r', min_redis_version,
                '-rl', min_rlec_version]

        metadata = module_packer.set_defaults(MODULE_FILE_PATH)
        module_packer.cmd_mode(metadata, argv)

        self.assertEqual(metadata["module_name"], "")
        self.assertEqual(metadata["module_file"], MODULE_FILE)
        self.assertEqual(metadata["architecture"], 64)
        self.assertEqual(metadata["version"], "1.0")
        self.assertEqual(metadata["author"], author)
        self.assertEqual(metadata["email"], email)
        self.assertEqual(metadata["description"], description)
        self.assertEqual(metadata["homepage"], homepage)
        self.assertEqual(metadata["license"], _license)
        self.assertEqual(metadata["extra_files"], extra_files)
        self.assertEqual(metadata["command_line_args"], command_line_args)
        self.assertEqual(metadata["min_redis_version"], min_redis_version)
        self.assertEqual(metadata["min_rlec_version"], min_rlec_version)
        self.assertEqual(metadata["sha256"], sha256_checksum(MODULE_FILE_PATH))

        commands = metadata["commands"]
        # self.validate_module_commands(commands)

    def test_output(self):
        """Test to see if bundle file gets generated"""
        try:
            os.remove(BUNDLE_ZIP_FILE)
        except OSError:
            pass

        metadata = module_packer.set_defaults(MODULE_FILE_PATH)
        module_packer.archive(MODULE_FILE_PATH, metadata)
        self.assertTrue(os.path.isfile(BUNDLE_ZIP_FILE))



if __name__ == '__main__':
    unittest.main()
