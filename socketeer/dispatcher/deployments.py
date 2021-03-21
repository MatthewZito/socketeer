from time import sleep

from ..utils.io import broadcast, log

def deploy_tasks(srv, commit_sha):
    """Deploy tasks for given commit shasum

    Args:
        srv: dispatch server instance 
        commit_sha (str): commit shasum / id correlated to given task
    """
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
                # record which thread is handling given shasum task
                srv.dispatched_commits[commit_sha] = runner

                if commit_sha in srv.pending_commits:
                    srv.pending_commits.remove(commit_sha)
                return
                
        sleep(9)