import json
import re
from zipfile import ZipFile, BadZipfile
from typing import Dict, Any, IO, Tuple, Optional  # noqa: F401
from .common import *


INVALID_METADATA = "module metadata invalid"
DEFAULT_MAX_MODULE_FILE_SIZE = 1024 * 1024 * 10


class UnpackerPackageError(Exception):
    """
    Represents an error within the unpacking process
    """

    def __init__(self, message, reason=None, error_code=None, error_details=None):
        # type: (str, Optional[str], Optional[str], Dict[str, Any]) -> None
        super(UnpackerPackageError, self).__init__(message)
        self.reason = reason
        self.error_code = error_code
        self.error_details = error_details

    def __str__(self):
        # type: () -> str
        return "{}, reason: {}".format(super(UnpackerPackageError, self).__str__(), self.reason)


def unpack(bundle, max_bundle_size_mb=None):
    # type: (IO[bytes], Optional[int]) -> Tuple[Dict[str, Any], IO[bytes]]
    """
    Unpacks a bundled module, performs sanity validation on bundle.
    both the module metadata and the actual module are returned
    :rtype: tuple
    """
    try:
        with ZipFile(bundle) as zf:
            _validate_zip_file(zf, max_bundle_size_mb)
            metadata = json.load(zf.open('module.json'))
            module = zf.open(metadata["module_file"])
            _validate_metadata(metadata)

    except BadZipfile:
        raise UnpackerPackageError(message="Failed to extract bundle")

    except (IOError, ValueError):
        raise UnpackerPackageError("Failed to read module.json")

    except UnpackerPackageError:  # re-raise exceptions raised by validator-methods
        raise

    return metadata, module


def _validate_zip_file(zip_file, max_bundle_size_mb):
    # type: (ZipFile, Optional[int]) -> None
    """
    Checks if all entries within the zip file don't
    exceed a certain threshold.
    """
    infolist = zip_file.infolist()
    # We're expecting exactly two files.
    if len(infolist) != 2:
        raise UnpackerPackageError(message="module zip file content invalid",
                                   reason="module zip file should contains exactly two file",
                                   error_code="invalid_number_of_files")

    file_size_limit_bytes = max_bundle_size_mb * 1024 * 1024 if max_bundle_size_mb else DEFAULT_MAX_MODULE_FILE_SIZE

    # Check zip content size.
    for zip_info in infolist:
        # Size of the compressed/uncompressed data.
        if zip_info.file_size > file_size_limit_bytes:
            raise UnpackerPackageError(message="module zip file did not pass sanity validation",
                                       reason="module file content is too big",
                                       error_code="module_size_too_big",
                                       error_details={'module_size': zip_info.compress_size,
                                                      'max_size': file_size_limit_bytes})


def _validate_metadata(metadata):
    # type: (Dict[str, Any]) -> None
    """
    Checks metadata isn't missing any required fields
    :param metadata: dictionary
    :raises: UnpackerPackageError
    """

    if not metadata["module_name"]:
        raise UnpackerPackageError(message=INVALID_METADATA,
                                   reason="Empty module name",
                                   error_code="module_name_missing")

    if not metadata["module_file"]:
        raise UnpackerPackageError(message=INVALID_METADATA,
                                   reason="Empty module file name",
                                   error_code="module_file_missing")

    if metadata["architecture"] != 'x86_64':
        raise UnpackerPackageError(message=INVALID_METADATA,
                                   reason="Architecture must be 64 bits",
                                   error_code="module_architecture_not_supported",
                                   error_details={'expected': 'x86_64'})

    if not metadata["version"]:
        raise UnpackerPackageError(message=INVALID_METADATA,
                                   reason="Missing version",
                                   error_code="module_version_missing")

    try:
        metadata["version"] = int(float(metadata["version"]))
    except (ValueError, TypeError):
        raise UnpackerPackageError(message=INVALID_METADATA,
                                   reason="Module version should be an integer",
                                   error_code="module_version_not_integer")

    if "os_list" in metadata:
        try:
            metadata["os_list"] = [_os_version_parser(os) for os in metadata["os_list"]]
        except UnpackerPackageError:
            raise

    # wrong signature
    # TODO: this check should be deferred to a later stage
    # As sha256_checksum will read entire module file
    # And we're unable to seek it back to its starting point.
    # if sha256_checksum(module) != metadata["sha256"]:
    # [If needed, use module_metadata.sha256_checksum]
    #     raise UnpackerPackageError(message="module did not pass sanity validation",
    #                                reason="Wrong signature")


def _os_version_parser(os_version):
    # type: (str) -> Dict[str, str]
    """
    Parses an OS version string from the RAMP file to the same format as in the distro package
    :param os_version: a string in the format of the RAMP file, e.g. 'ubuntu18.04'
    :return: dictionary with the keys 'name' and 'version', for the OS name and OS version.
    """
    try:
        name_matcher = re.search(r'[a-zA-Z_]+', os_version)
        version_matcher = re.search(r'(\d+)(\.\d+)?(\.\d+)?', os_version)
        assert name_matcher and version_matcher
        name = name_matcher.group(0)
        version = version_matcher.group(0)
    except (ValueError, TypeError, AssertionError):
        raise UnpackerPackageError(message=INVALID_METADATA,
                                   reason="Can't parse OS '{}'".format(os_version),
                                   error_code="module_os_list_invalid")
    return {'name': name, 'version': version}
