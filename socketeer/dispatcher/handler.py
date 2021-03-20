from re import compile, findall
from os import path, makedirs

from socketserver import BaseRequestHandler

from ..utils.log import log
from .deployments import deploy_tasks

def log_info(directive):
  log(
    level='info',
    message=f'recv {directive} directive'
  )

class DispatchHandler(BaseRequestHandler):
  """
  A request handler for the dispatch srv

  Dispatch task runners against incoming commit SHAs and handle results thereof
  """
  cmd_regexp = compile(r'(\w+)(:.+)*')

  BUF_SIZE = 1024

  def handler(self):
    self.data = self.request.recv(self.BUF_SIZE).strip()
    cmd_grp = self.cmd_regexp.match(self.data)

    if not cmd_grp:
      self.request.sendall('Invalid command')
      return
    
    directive, payload = cmd_grp.groups()

    if directive == 'STATUS':
      self.dispatch_ping()
      
    elif directive == 'REGISTER':
      self.dispatch_registrar(payload)

    elif directive == 'DISPATCH':
      self.dispatch_tasks(payload)

    elif directive == 'RESULTS':
      self.dispatch_results(payload)

    else:
      self.request.sendall('Invalid command')


  def dispatch_ping(self):
    log_info('status')
    self.request.sendall('OK')

  def dispatch_registrar(self, payload):
    log_info('register')
      
    host, port = findall(r':(\w*)', payload)

    self.server.runners.append({
      'host': host,
      'port': port
    })

    self.request.sendall('OK')

  def dispatch_tasks(self, payload):
    log_info('dispatch')

    commit_sha = payload[1:]

    if not self.server.runners:
      self.request.sendall('No task runners are registered')
    else:
      self.request.sendall('OK')
      deploy_tasks(
        self.server,
        commit_sha
      )

  def dispatch_results(self, payload):
    log_info('results')

    commit_sha, res = payload[1:].split(':')
    msg_len = int(res)

    remaining_buffer = self.BUF_SIZE - (len('results') + len(commit_sha) + len(res) + 3)

    if msg_len > remaining_buffer:
      self.data += self.request.recv(msg_len - remaining_buffer).strip()
    del self.server.dispatched_commits[commit_sha]

    if not path.exists('test_results'):
      makedirs('test_results')
    with open('test_results' + '/' + commit_sha, 'w') as f:
      data = '\n'.join(self.data.split(':')[3:])
      f.write(data)

    self.request.sendall('OK')
  
