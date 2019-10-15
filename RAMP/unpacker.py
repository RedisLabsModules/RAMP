import json
from zipfile import ZipFile, BadZipfile
import semantic_version
from typing import Dict, Any, IO, Tuple, Optional  # noqa: F401

from RAMP import module_metadata
from distutils.version import StrictVersion

MAX_MODULE_FILE_SIZE = 1024 * 1024 * 10


class UnpackerPackageError(Exception):
    """
    Represents an error within the unpacking process
    """

    def __init__(self, message, reason=None):
        # type: (str, Optional[str]) -> None
        super(UnpackerPackageError, self).__init__(message)
        self.reason = reason

    def __str__(self):
        # type: () -> str
        if self.reason:
            return "{}, reason: {}".format(super(UnpackerPackageError, self).__str__(), self.reason)
        else:
            return "{}".format(super(UnpackerPackageError, self).__str__())


def unpack(bundle):
    # type: (IO[bytes]) -> Tuple[Dict[str, Any], IO[bytes]]
    """
    Unpacks a bundled module, performs sanity validation
    on bundle.
    :return:
    :rtype: tuple
    both the module metadata and the actual module are returned
    """

    # Extract.
    try:
        with ZipFile(bundle) as zf:
            # validate_zip_file throws
            # we want this exception to propagate
            _validate_zip_file(zf)

            try:
                metadata = json.load(zf.open('module.json'))
            except (IOError, ValueError):
                raise UnpackerPackageError("Failed to read module.json")

            module = zf.open(metadata["module_file"])

            # _validate throws in case of an error,
            # we want this exception to propagate
            _validate_metadata(metadata)

    except BadZipfile:
        raise UnpackerPackageError("Failed to extract bundle")

    return metadata, module


def _validate_zip_file(zip_file):
    # type: (ZipFile) -> True
    """
    Checks if all entries within the zip file don't
    exceed a certain threshold.
    """
    infolist = zip_file.infolist()
    # We're expecting exactly two files.
    if len(infolist) != 2:
        raise UnpackerPackageError(message="module zip file did not pass sanity validation",
                                   reason="module zip file should contains exactly two file")

    # Check zip content size.
    for zip_info in infolist:
        # Size of the compressed/uncompressed data.
        if zip_info.file_size > MAX_MODULE_FILE_SIZE:
            raise UnpackerPackageError(message="module zip file did not pass sanity validation",
                                       reason="module file content is too big")

    return True


def _validate_metadata(metadata):
    # type: (Dict[str, Any]) -> bool
    """
    Checks metadata isn't missing any required fields
    metadata - dictionary
    module - path to module file
    """

    for field in module_metadata.FIELDS:
        if field not in metadata:
            raise UnpackerPackageError(message="module did not pass sanity validation",
                                       reason="Missing mandatory field [{}]".format(field))

    # Empty module name
    if metadata["module_name"] == "":
        raise UnpackerPackageError(message="module did not pass sanity validation",
                                   reason="Empty module name")

    # Empty module file name
    if metadata["module_file"] == "":
        raise UnpackerPackageError(message="module did not pass sanity validation",
                                   reason="Empty module file name")

    # Architecture must 64 bits
    if metadata["architecture"] != "x86_64":
        raise UnpackerPackageError(message="module did not pass sanity validation",
                                   reason="Architecture must 64 bits")

    # Missing version
    if not semantic_version.validate(metadata["semantic_version"]):
        raise UnpackerPackageError(message="module did not pass sanity validation",
                                   reason="Invalid semantic version")

    if StrictVersion(metadata["min_redis_pack_version"]) < StrictVersion(module_metadata.MIN_REDIS_PACK_VERSION):
        raise UnpackerPackageError(message="module did not pass sanity validation",
                                   reason="Min redis pack version is too low")

    # wrong signature
    # TODO: this check should be deferred to a later stage
    # As sha256_checksum will read entire module file
    # And we're unable to seek it back to its starting point.
    # if sha256_checksum(module) != metadata["sha256"]:
    # [If needed, use module_metadata.sha256_checksum]
    #     raise UnpackerPackageError(message="module did not pass sanity validation",
    #                                reason="Wrong signature")

    return True
