import pkg_resources
try:
    VERSION = pkg_resources.get_distribution("ramp-packer").version
except:
    VERSION = "99.99.99"
