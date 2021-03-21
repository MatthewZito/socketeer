import os
import re
import socketserver
import subprocess
import time
import unittest

from ..utils.constants import \
    MESSAGES as msg, \
    PRE_TASK as script, \
    ROOT_SCRIPTS_DIR as root, \
    TMP_RESULTS as tmp_f
from ..utils.io import broadcast, log

class TaskHandler(socketserver.BaseRequestHandler):
    """Handle task requests from dispatch

    Args:
        BaseRequestHandler
    """

    cmd_regexp = re.compile(r'(\w+)(:.*)*')

    def handle_request(self):
        """Request handler for a given task-runner instance / thread
        """
        self.data = self.request.recv(1024).strip()

        cmd_grp = self.cmd_regexp.match(self.data)
        cmd = cmd_grp.group(1)

        if not cmd:
            self.request.sendall('Invalid command')
            return

        if cmd == msg['PING']:
            log(
                level='warn',
                message='Liveness check received; responding...'
            )
            self.server.last_conn = time.time()
            self.request.sendall(msg['ACK'])

        elif cmd == msg['RUNTASK']:
            log(
                level='warn',
                message=f'Task received; thread busy? {self.server.busy}'
            )
            if self.server.busy:
                self.request.sendall('BUSY')

            # thread not busy, proceed
            else:
                self.request.sendall('OK')
                log(
                    level='warn',
                    message='Thread now executing task...'
                )
                sha = cmd_grp.group(2)[1:]
                self.server.busy = True
                self.execute_tasks(
                    sha,
                    self.server.repo_dir
                )

        else:
            self.request.sendall('Invalid command')


    def execute_tasks(self, sha, repo_dir):
        """Execute tasks for given commitexecute_tasks

        Args:
            sha (str): commit sha representing state at which to execute tasks
            repo_dir (str): path to target repository
        """
        script_path = f'{root}/{script}'
        # update repository clone
        stdout = subprocess.check_output([
            script_path,
            repo_dir,
            sha
        ])

        log(
            level='warn',
            message=stdout
        )

        tasks_dir = os.path.join(repo_dir, 'tasks')
        suite = unittest.TestLoader().discover(tasks_dir)
        results_f = open(tmp_f, 'w')
        unittest.TextTestRunner(results_f).run(suite)

        results_f.close()

        results_f = open(tmp_f, 'r')
        # pass task execution results to dispatch
        out = results_f.read()
        broadcast(
            self.server.dispatch_srv['host'],
            int(self.server.dispatch_srv['port']),
            msg['RESULTS'] + msg['DELIMITER'] + (sha, len(out), out)
        )
