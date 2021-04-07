"""Serve the Dispatch Srv; handle Task-Runner threads and Observer messages"""
import threading

from ..thread_mon.failover import redistribute_orphan_task

from ..thread_mon.liveness import check_liveness

from ..utils.constants import MESSAGES as msg
from ..utils.io import log

from .cli import get_args
from .handler import DispatchHandler
from .Threading_TCP_srv import ThreadingTCPSrv

def serve():
    """Dispatcher
    Handle correspondence between threaded task-runners and observer srv requests

    Spawn task redistributor and runner liveness eval threads
    """
    args = get_args()
    host, port = args.dispatch.split(msg['DELIMITER'])

    srv = ThreadingTCPSrv(
        (host, int(port)),
        DispatchHandler
    )

    log(
        type='warn',
        message=f'Listening on {host}:{port}...'
    )

    # spawn thread to manage liveness checks
    heart_beat = threading.Thread(
        target=check_liveness,
        args=(srv,)
    )

    # spawn thread to redistribute orphaned tasks
    redistributor = threading.Thread(
        target=redistribute_orphan_task,
        args=(srv,)
    )

    try:
        heart_beat.start()
        redistributor.start()
        srv.serve_forever()

    except (KeyboardInterrupt, Exception):
        srv.dead = True
        heart_beat.join()
        redistributor.join()

        log(
            level='warn',
            message=f'Dispatch srv at {host}:{port} died...'
        )
