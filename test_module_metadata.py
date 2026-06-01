import os
import tempfile
import unittest
from unittest import mock

from RAMP import module_metadata


class GetCurrOsTest(unittest.TestCase):
    def test_uses_devcontainer_distro_before_host_distro(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            devcontainer_path = os.path.join(temp_dir, "devcontainer")
            with open(devcontainer_path, "w") as f:
                f.write("DISTRO=amzn2023\n")

            with mock.patch.object(module_metadata, "DEVCONTAINER_PATH", devcontainer_path):
                with mock.patch.object(module_metadata.distro, "id", return_value="rocky"):
                    with mock.patch.object(module_metadata.distro, "version_parts", return_value=("8",)):
                        self.assertEqual(module_metadata.get_curr_os(), "amzn2023")

    def test_falls_back_to_distro_when_devcontainer_has_no_distro(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            devcontainer_path = os.path.join(temp_dir, "devcontainer")
            with open(devcontainer_path, "w") as f:
                f.write("OTHER=value\n")

            with mock.patch.object(module_metadata, "DEVCONTAINER_PATH", devcontainer_path):
                with mock.patch.object(module_metadata.distro, "id", return_value="rocky"):
                    with mock.patch.object(module_metadata.distro, "version_parts", return_value=("8",)):
                        self.assertEqual(module_metadata.get_curr_os(), "rhel8")

    def test_preserves_distro_fallback_when_devcontainer_is_absent(self):
        devcontainer_path = os.path.join(tempfile.gettempdir(), "missing-devcontainer")
        with mock.patch.object(module_metadata, "DEVCONTAINER_PATH", devcontainer_path):
            with mock.patch.object(module_metadata.distro, "id", return_value="ubuntu"):
                with mock.patch.object(module_metadata.distro, "version_parts", return_value=("22",)):
                    self.assertEqual(module_metadata.get_curr_os(), "ubuntu22")


if __name__ == "__main__":
    unittest.main()
