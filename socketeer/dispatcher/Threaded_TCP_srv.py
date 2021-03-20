from socketserver import ThreadingMixIn, TCPServer

class ThreadingTCPSrv(ThreadingMixIn, TCPServer):
  # track task runner pool
  runners = []
  # flag - indicates to threads whether srv is live
  dead = False
  # track commits for which tasks have been dispatched
  dispatched_commits = {}
  # track commits for which tasks have yet to be dispatched
  pending_commits = [] 
