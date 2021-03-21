import time
import socket

from ..utils.io import broadcast, log
from ..utils.constants import MESSAGES as msg

def dispatch_chk(srv):
    """Check if dispatch service is live. If not, shut down given it may
    not have same host/port once it goes live again
    """
    time.sleep(6)
    if (time.time() - srv.last_conn) > 10:
        try:
            response = broadcast(
                srv.dispatch_srv['host'],
                int(srv.dispatch_srv['port']),
                msg['STATUS']
            )

            if response != msg['OK']:
                log(
                    level='error',
                    message='Dispatch srv has died'
                )

                srv.shutdown()
                return

        except socket.error as e:
            log(
                level='error',
                message='Dispatch srv conn error: ' + e
            )
            srv.shutdown()
            return
