
from __future__ import print_function
import sys
import os


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def normalize_dependencies(deps):
    if isinstance(deps, dict):
        for dep_name, dep in deps.items():
            for key in ["url", "sha256"]:
                if key not in dep:
                    raise Exception("error: dependency {} missing {}".format(dep_name, key))
    elif isinstance(deps, list):
        deps_list = deps
        deps = {}
        for dep in deps_list:
            for key in ["name", "url", "sha256"]:
                if key not in dep:
                    raise Exception("error: dependency missing {}".format(key))
            deps[dep["name"]] = { k:v for k, v in dep.items() if k != "name" }
    else:
        raise Exception("error: invalid dependencies format")
    return deps
