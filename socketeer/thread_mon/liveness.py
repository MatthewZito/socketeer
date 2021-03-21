from socket import socket, error, AF_INET, SOCK_STREAM
from time import sleep

from ..utils.io import broadcast, log
from ..utils.constants import MESSAGES as msg

from .failover import manage_tasks_pool

def check_liveness(srv):
    while not srv.dead:
        sleep(1)
        for runner in srv.runners:
            s = socket(
                AF_INET,
                SOCK_STREAM
            )

            try:
                host, port = runner['host'], int(runner['port'])

                response = broadcast(
                    host,
                    port,
                    'PING'
                )

                if response != msg['ACK']:
                    log(
                        level='warn',
                        message=f'Thread at {host}:{port} failed liveness check. Removing from pool and reallocating task...'
                    )

                    manage_tasks_pool(srv, runner)

            except error:
                manage_tasks_pool(srv, runner)
