import semantic_version

MAJOR_VERSION = 1
MINOR_VERSION = 3
PATCH_VERSION = 8
VERSION = semantic_version.Version('{}.{}.{}'.format(MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION))