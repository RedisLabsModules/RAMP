
from __future__ import print_function
import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def normalize_dependencies(deps):
    if isinstance(deps, dict):
        for dep_name, dep in deps.items():
            for key in ["url", "sha256"]:
                if key not in dep:
                    raise Exception("error: dependency {} missing {}".format(dep_name, key))
    elif isinstance(deps, list):
        deps_dict = {}
        for dep in deps:
            for key in ["name", "url", "sha256"]:
                if key not in dep:
                    raise Exception("error: dependency missing {}".format(key))
            deps_dict[dep["name"]] = { k:v for k, v in dep.items() if k != "name" }
        return deps_dict
    else:
        raise Exception("error: invalid dependencies format")
