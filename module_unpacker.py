import os
import sys
import json
import zipfile
import hashlib
from RAMP import module_metadata
from distutils.version import StrictVersion

MAX_MODULE_FILE_SIZE = 1024 * 1024 * 10

class UnpackerPackageError(Exception):
    """
    Represents and error within the unpacking process
    """
    def __init__(self, message, reason=None):
        super(UnpackerPackageError, self).__init__(message)
        self.reason = reason

    def __str__(self):
        return "{}, reason: {}".format(super(UnpackerPackageError, self).__str__(), self.reason)

def _sha256_checksum(module_file):
    """Computes sha256 for given file"""

    sha256 = hashlib.sha256()
    sha256.update(module_file.read())
    return sha256.hexdigest()

def unpack(bundle):
    """
    Unpacks a bundeled module, performs sanity validation
    on bundle.
    :return:
    :rtype: tuple
    both the module metadata and the actual module are returned
    """

    # Extract.
    try:
        with zipfile.ZipFile(bundle) as zf:
            # _validate_zip_file throws
            # we want this exception to propagate
            _validate_zip_file(zf)

            try:
                metadata = json.load(zf.open('module.json'))
            except IOError, ValueError:
                raise UnpackerPackageError("Failed to read module.json")

            module = zf.open(metadata["module_file"])

            # _validate throws incase of an error,
            # we want this exception to propagate
            _validate(metadata, module)

    except zipfile.BadZipfile:
        raise UnpackerPackageError("Failed to extract bundle")

    return (metadata, module)

def _validate_zip_file(zip_file):
    """
    Checks if all entries within the zip file don't
    exceed a certian threshold.
    """
    infolist = zip_file.infolist()
    # We're expecting exactly two files.
    if len(infolist) != 2:
        raise UnpackerPackageError("module zip file did not pass sanity validation", reason="module zip file should contains exactly two file")

    # Check zip content size.
    for zipinfo in infolist:
        # Size of the compressed/uncompressed data.
        if zipinfo.compress_size > MAX_MODULE_FILE_SIZE or zipinfo.file_size > MAX_MODULE_FILE_SIZE:
            raise UnpackerPackageError("module zip file did not pass sanity validation", reason="module zip content is too big")

    return True

def _validate(metadata, module):
    """
    Checks metadata isn't missing any required fields
    metadata - dictionary
    module - path to module file
    """

    for field in module_metadata.FIELDS:
        if not field in metadata:
            raise UnpackerPackageError("module did not pass sanity validation", reason="Missing mandatory field [{}]".format(field))

    # Empty module name
    if metadata["module_name"] == "":
        raise UnpackerPackageError("module did not pass sanity validation", reason="Empty module name")

    # Empty module file name
    if metadata["module_file"] == "":
        raise UnpackerPackageError("module did not pass sanity validation", reason="Empty module file name")

    # Architecture must 64 bits
    if metadata["architecture"] != "x86_64":
        raise UnpackerPackageError("module did not pass sanity validation", reason="Architecture must 64 bits")

    # Missing version
    if metadata["version"] == "":
        raise UnpackerPackageError("module did not pass sanity validation", reason="Missing version")

    if StrictVersion(metadata["min_redis_version"]) < StrictVersion(module_metadata.MIN_REDIS_VERSION):
        raise UnpackerPackageError("module did not pass sanity validation", reason="Min Redis version is too low")

    if StrictVersion(metadata["min_rlec_version"]) < StrictVersion(module_metadata.MIN_RLEC_VERSION):
        raise UnpackerPackageError("module did not pass sanity validation", reason="Min RLEC version is too low")

    # wrong signature
    # TODO: this check should be deffered to a later stage
    # As _sha256_checksum will read entire module file
    # And we're unable to seek it back to its starting point.
    # if _sha256_checksum(module) != metadata["sha256"]:
    #     raise UnpackerPackageError("module did not pass sanity validation", reason="Wrong signature")

    return True
