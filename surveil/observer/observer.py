"""The Observer module watches a target git repository for changes
and adds commit ids to the tasks pool by communicating with the Dispatch Srv
on-change.
"""
import os
import socket
import subprocess
import time

from ..utils.constants import \
    COMMIT_SHA as commit, \
    GET_LATEST as script, \
    INTERVAL as interval, \
    MESSAGES as msg, \
    ROOT_SCRIPTS_DIR as root
from ..utils.io import broadcast, log

from .cli import get_args

def poll ():
    """Poll the target repository at *interval* of seconds

    Check for new commits to target repository and notify dispatch srv of changes
    by way of new commit SHAs

    Broadcast notifications to dispatch srv with said commit SHA to initialize tests
    """
    args = get_args()
    host, port = args.dispatch.split(msg['DELIMITER'])
    repo = args.repository

    script_path = f'{root}/{script}'

    while True:
        # execute shell script to pull repository, check for new commits
        # persists commit SHA in tmp file in cwd if applicable
        try:
            subprocess.check_output([
                script_path,
                repo
            ])

        except OSError as ex:
            if ex.errno == 2:
                raise FileNotFoundError(f'{script_path} was not found') from ex
            raise Exception(
                'An I/O error occurred ' +
                ex
            ) from ex

        except subprocess.CalledProcessError as ex:
            raise Exception(
                'Unable to update and observe repository ' +
                ex.output.decode('utf-8', errors='ignore')
            ) from ex

        if os.path.isfile(commit):
            # repository state has changed
            try:
                # check dispatch srv liveness
                response = broadcast(
                    host,
                    int(port),
                    msg['STATUS'] + msg['DELIMITER']
                )

            except socket.error as ex:
                raise ConnectionError (
                    'Unable to ping dispatch srv'
                ) from ex

            if response == msg['OK']:
                # dispatch srv is live
                commit_sha = ''
                with open(commit, 'r') as f:
                    commit_sha = f.readline()
                    # initialize tasks
                    response = broadcast(
                        host,
                        int(port),
                        msg['DISPATCH'] + msg['DELIMITER'] + commit_sha
                    )

                    if response != msg['OK']:
                        raise ConnectionError(
                            'Unable to broadcast to dispatch srv ' +
                            response
                        )

                    log(
                        level='success',
                        message='Dispatch directive successfully broadcast'
                    )

            else:
                raise ConnectionError(
                    'Unable to connect to dispatch srv ' +
                    response
                )
        time.sleep(interval)
