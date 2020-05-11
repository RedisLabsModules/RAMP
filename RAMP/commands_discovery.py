import os.path

from RAMP.disposableredis import DisposableRedis
from RAMP import config
from .common import *

OK = "OK"

class Module(object):
    def __init__(self, module_name, module_version):
        self.name = module_name
        self.version = module_version
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

class ModuleCommand(object):
    def __init__(self, command_name, command_arity, flags, first_key, last_key, step):
        self.command_name = command_name
        self.command_arity = command_arity
        self.flags = flags
        self.first_key = first_key
        self.last_key = last_key
        self.step = step

    def to_dict(self):
        return self.__dict__

def redis():
    redis_client = DisposableRedis(verbose=config.debug)
    return redis_client

def _get_modules_list(redis_client):
    """
    Finds out which modules are loaded into Redis.
    """
    modules_list = redis_client.execute_command("MODULE LIST")
    # MODULE LIST response contains an array of module name and version.
    #    1) 1) "name"
    #       2) "graph"
    #       3) "ver"
    #       4) (integer) 1

    loaded_modules = []
    for module in modules_list:
        module_name = module[1]
        module_version = float(module[3])
        loaded_modules.append((module_name, module_version))

    return loaded_modules

def _load_module(redis_client, path_to_module, module_args):
    """
    Loads given module to redis.
    :redis_client: open connection to redis
    :param path_to_module: where does the module file is located.
    Assuming only a single module is loaded.
    """
    resp = redis_client.execute_command("MODULE LOAD {} {}".format(
        os.path.abspath(path_to_module), module_args))
    if resp != OK:
        return None

    loaded_modules = _get_modules_list(redis_client)
    if len(loaded_modules) != 1:
        return None

    loaded_modules = loaded_modules[0]
    return Module(loaded_modules[0], loaded_modules[1])

def _get_redis_commands(redis_client):
    """
    Retrieves a set of commands from Redis
    """
    commands = redis_client.execute_command("COMMAND")
    redis_commands = set()
    for command in commands:
        redis_commands.add(command[0])
    return redis_commands

def _get_redis_command_info(redis_client, command_name):
    """
        Retrieves command info from Redis
        Returns ModuleCommand
    """
    command_info = redis_client.execute_command("COMMAND INFO {}".format(command_name))
    # 1) 1) "graph.ADDEDGE"
    #    2) (integer) -1
    #    3) 1) write
    #    4) (integer) 1
    #    5) (integer) 1
    #    6) (integer) 1

    if len(command_info) is not 1:
        return None

    command_info = command_info[0]

    command_name = command_info[0]
    command_arity = command_info[1]
    flags = command_info[2]
    first_key = command_info[3]
    last_key = command_info[4]
    step = command_info[5]

    return ModuleCommand(command_name, command_arity, flags, first_key, last_key, step)

def discover_modules_commands(path_to_module, module_args):
    """
        Retrieves module command(s) info.
        :param path_to_module: where does the module file is located
        Returns Module object populated with command(s) info.
    """
    with redis() as redis_client:
        core_redis_commands = _get_redis_commands(redis_client)
        module = _load_module(redis_client, path_to_module, module_args)
        if module is None:
            raise Exception("Failed to load module {} {}".format(path_to_module, module_args))

        extended_redis_commands = _get_redis_commands(redis_client)
        module_commands = extended_redis_commands - core_redis_commands

        for module_command in module_commands:
            command = _get_redis_command_info(redis_client, module_command)
            if command is None:
                raise Exception("Failed to retreive command info for {}".format(module_command))

            module.add_command(command)

        return module
