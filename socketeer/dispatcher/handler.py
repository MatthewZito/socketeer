"""This module provides a request handler for the Dispatch Srv"""
import os
import re
import socketserver

from ..utils.constants import MESSAGES as msg, \
    TASK_RESULTS as result_f
from ..utils.io import log

from .deployments import deploy_tasks

def log_info(directive):
    """Log warn level message indicating received directive

    Args:
        directive (str): received directive
    """
    log(
        level='warn',
        message=f'recv {directive} directive'
    )

class DispatchHandler(socketserver.BaseRequestHandler):
    """
    A request handler for the dispatch srv

    Dispatch task runners against incoming commit SHAs and handle results thereof
    """
    cmd_regexp = re.compile(r'(\w+)(:.+)*')

    BUF_SIZE = 1024

    def handler(self):
        """Handle requests from Observer, Task-Runner threads
        """
        self.data = self.request.recv(self.BUF_SIZE).strip()
        cmd_grp = self.cmd_regexp.match(self.data)

        if not cmd_grp:
            self.request.sendall('Invalid command')
            return

        directive, payload = cmd_grp.groups()

        if directive == msg['STATUS']:
            self.dispatch_status_chk()

        elif directive == msg['REGISTER']:
            self.dispatch_registrar(payload)

        elif directive == msg['DISPATCH']:
            self.dispatch_tasks(payload)

        elif directive == msg['RESULTS']:
            self.dispatch_results(payload)

        else:
            self.request.sendall('Invalid command')


    def dispatch_status_chk(self):
        """Respond to status check request
        """
        log_info('status')
        self.request.sendall(msg['OK'])

    def dispatch_registrar(self, payload):
        """Respond to registration request; register new task-runner thread

        Args:
            payload (str): a payload containing the pending task-runner thread's host, port
        """
        log_info('register')

        host, port = re.findall(r':(\w*)', payload)

        self.server.runners.append({
            'host': host,
            'port': port
        })

        self.request.sendall(msg['OK'])

    def dispatch_tasks(self, payload):
        """Fetch commit shasum and deploy task spawn

        Args:
            payload (str): a payload containing the commit shasum for which to dispatch a new task
        """
        log_info('dispatch')

        commit_sha = payload[1:]

        if not self.server.runners:
            self.request.sendall('No task runners are registered')
        else:
            self.request.sendall(msg['OK'])
            deploy_tasks(
                self.server,
                commit_sha
            )

    def dispatch_results(self, payload):
        """Respond to request for task results; write to file

        Args:
            payload (str): buffered results payload
        """
        log_info('results')

        commit_sha, res = payload[1:].split(msg['DELIMITER'])
        msg_len = int(res)

        remaining_buffer = self.BUF_SIZE - (len('results') + len(commit_sha) + len(res) + 3)

        if msg_len > remaining_buffer:
            self.data += self.request.recv(msg_len - remaining_buffer).strip()

        del self.server.dispatched_commits[commit_sha]

        if not os.path.exists(result_f):
            os.makedirs(result_f)

        with open(result_f + '/' + commit_sha, 'w') as f:
            data = '\n'.join(self.data.split(msg['DELIMITER'])[3:])
            f.write(data)

        self.request.sendall(msg['OK'])
