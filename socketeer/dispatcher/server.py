from threading import Thread

from ..utils.io import log
from ..utils.constants import MESSAGES as msg

from ..thread_mon.failover import \
  	manage_tasks_pool, \
  	redistribute_orphan_task

from ..thread_mon.liveness import check_liveness

from .cli import get_args
from .handler import DispatchHandler
from .Threading_TCP_srv import ThreadingTCPSrv

def serve():
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
	heart_beat = Thread(
		target=check_liveness,
		args=(srv,)
	)

	# spawn thread to redistribute orphaned tasks
	redistributor = Thread(
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