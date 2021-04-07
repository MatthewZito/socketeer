import socket
import time

from ..utils.constants import MESSAGES as msg
from ..utils.io import broadcast, log

from .failover import manage_tasks_pool

def check_liveness(srv):
    while not srv.dead:
        time.sleep(1)
        for runner in srv.runners:
            s = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            try:
                host, port = runner['host'], int(runner['port'])

                response = broadcast(
                    host,
                    port,
                    msg['PING']
                )

                if response != msg['ACK']:
                    log(
                        level='warn',
                        message=f'Thread at {host}:{port} failed liveness check. \
                            Removing from pool and reallocating task...'
                    )

                    manage_tasks_pool(srv, runner)

            except socket.error:
                manage_tasks_pool(srv, runner)
