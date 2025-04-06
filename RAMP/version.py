try:
    from importlib.metadata import version
    VERSION = version("ramp-packer")
except:
    VERSION = "99.99.99"
