import subprocess
import socket
import tempfile
import redis
import time
import os
import itertools
import sys

from ..common import *

# Environment variable pointing to the redis executable
REDIS_PATH_ENVVAR = 'REDIS_PATH'


def get_random_port():
    sock = socket.socket()
    sock.listen(0)
    _, port = sock.getsockname()
    sock.close()

    return port


class DisposableRedis(object):
    def __init__(self, port=None, path='redis-server', verbose=False, **extra_args):
        """
        :param port: port number to start the redis server on. Specify none to automatically generate
        :type port: int|None
        :param extra_args: any extra arguments kwargs will be passed to redis server as --key val
        """

        self._port = port
        self.verbose = verbose

        # this will hold the actual port the redis is listening on. It's equal to `_port` unless `_port` is None
        # in that case `port` is randomly generated
        self.port = None
        self.extra_args = list(itertools.chain(
                *(('--%s'%k, v) for k, v in extra_args.items())
               ))
        self.path = os.getenv(REDIS_PATH_ENVVAR, path)

    def _getRedisVersion(self):
        options = {
            'stderr': subprocess.PIPE,
            'stdin': subprocess.PIPE,
            'stdout': subprocess.PIPE,
        }
        p = subprocess.Popen(args=[self.path, '--version'], **options)
        while p.poll() is None:
            time.sleep(0.1)
        exit_code = p.poll()
        if exit_code != 0:
            raise Exception('Could not extract Redis version')
        out, err = p.communicate()
        out = out.decode('utf-8')
        v = out[out.find("v=") + 2:out.find("sha=") - 1].split('.')
        return int(v[0]) * 10000 + int(v[1]) * 100 + int(v[2])

    def __enter__(self):
        if self._port is None:
            self.port = get_random_port()
        else:
            self.port = self._port
        args = [self.path,
                '--port', str(self.port),
                '--dir', tempfile.gettempdir(),
                '--save', ''] + self.extra_args

        if self._getRedisVersion() >= 70000:
            args += ['--enable-module-command', 'yes']

        if self.verbose:
            out = sys.stdout
            err = sys.stderr
        else:
            out  = open(os.devnull, 'w')
            err = subprocess.STDOUT
        self.process = subprocess.Popen(
            args,
            #cwd=os.getcwd(),
            stdin=subprocess.PIPE,
            stdout=out,
            stderr=err,
            env=os.environ.copy(),
        )

        while True:
            try:
                self.client().ping()
                break
            except redis.ConnectionError:
                self.process.poll()
                if self.process.returncode is not None:
                    raise RuntimeError("Process has exited")
                time.sleep(0.1)

        return self.client()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.process.terminate()

    def client(self):
        """
        :rtype: redis.StrictRedis
        """

        return redis.StrictRedis(port=self.port, decode_responses=True)
