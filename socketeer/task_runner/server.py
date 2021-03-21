import errno
import socket
import threading

from ..utils.constants import \
    MESSAGES as msg, \
    RANGE_INIT as port_range

from ..thread_mon import dispatch_chk
from ..utils.io import broadcast, log

from .cli import get_args
from .Task_handler import TaskHandler
from .Threading_TCP_srv import ThreadingTCPSrv

def serve():
    args = get_args()

    runner_host = args.host
    runner_port = None
    attempts = 0

    if not args.port:
        runner_port = port_range

        while attempts < 100:
            try:
                srv = ThreadingTCPSrv(
                    (runner_host, runner_port),
                    TaskHandler
                )

                log(
                    level='warn',
                    message='fAttempting to spawn runner on port {runner_port}'
                )
                break

            except socket.error as e:
                if e.errno == errno.EADDRINUSE:
                    # bump attempts and try again
                    attempts += 1
                    runner_port = runner_port + attempts
                    continue

                raise e
        else:
            raise Exception('Exhausted allocated port range')

    # use given port
    else:
        runner_port = int(args.port)
        srv = ThreadingTCPSrv(
            (runner_host, runner_port),
            TaskHandler
        )

    srv.repo_dir = args.repo

    dispatch_host, dispatch_port = args.dispatch.split(':')
    srv.dispatch_srv = {
        'host': dispatch_host,
        'port': dispatch_port
    }

    response = broadcast(
        srv.dispatch_srv['host'],
        int(srv.dispatch_srv['port']),
        msg['REGISTER'] + msg['DELIMITER'] + (runner_host, runner_port)
    )

    if response != msg['OK']:
        raise Exception('Unable to register via dispatch srv')

    t = threading.Thread(
        target=dispatch_chk,
        args=(srv,)
    )

    try:
        # activate srv to eval liveness of dispatch
        t.start()
        srv.serve_forever()

    except (KeyboardInterrupt, Exception):
        # kill thread
        srv.dead = True
        t.join()
