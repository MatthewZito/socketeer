from time import sleep

from ..utils.log import log
from ..utils.io import broadcast

def deploy_tasks(srv, commit_sha):
  while True:
    log(
      level='warn',
      message='Preparing to dispatch tasks to runners'
    )

    for runner in srv.runners:
      response = broadcast(
        runner['host'],
        int(runner['port']),
        'RUNTASK:' + commit_sha
      )

      if response == 'OK':
        log(
          level='success',
          message='Adding SHA ' + commit_sha
        )

        srv.dispatched_commits[commit_sha] = runner
        if commit_sha in srv.pending_commits:
          srv.pending_commits.remove(commit_sha)

        return
      sleep(9)