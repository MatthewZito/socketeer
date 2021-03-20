from time import sleep

from ..utils.io import log
from ..dispatcher.deployments import deploy_tasks

"""
Handle dead threads.

Removes a given thread's (runner) current task, reallocate it to the pending pool.

Removes the thread reference from the server's thread pool.
"""
def manage_tasks_pool(srv, runner):
	for sha, assigned_thread in srv.dispatched_commits.iteritems():
		if assigned_thread == runner:
			del srv.dispatched_commits[sha]
			srv.pending_commits.append(sha)
			break

	srv.runners.remove(runner)

def redistribute_orphan_task(srv):
	while not srv.dead:
		for sha in srv.pending_commits:
			log(
				level='warn',
				message='Reallocating orphan tasks'
			)
			log(
				level='warn',
				message='Remaining tasks: ' + srv.pending_commits
			)
			
			deploy_tasks(srv, sha)
			sleep(6)