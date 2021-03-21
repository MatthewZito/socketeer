from socketserver import ThreadingMixIn, TCPServer

class ThreadingTCPSrv(ThreadingMixIn, TCPServer):
    """Socket server instance for handling multi-threaded concurrency

    Args:
        ThreadingMixIn (tuple)
        TCPServer (class): Socket-server base class
    """
    # track task runner pool
    runners = []
    # flag - indicates to threads whether srv is live
    dead = False
    # track commits for which tasks have been dispatched
    dispatched_commits = {}
    # track commits for which tasks have yet to be dispatched
    pending_commits = []
