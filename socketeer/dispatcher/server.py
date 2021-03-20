

from ..utils.log import log
from .cli import get_args
from .handler import DispatchHandler

from .Threaded_TCP_srv import ThreadingTCPSrv

def serve():
  args = get_args()
  host, port = args.dispatch.split(':')
  
  srv = ThreadingTCPSrv(
    (host, int(port)),
    DispatchHandler
  )

  log(
    type='warn',
    message='Serving on ' + port
  )