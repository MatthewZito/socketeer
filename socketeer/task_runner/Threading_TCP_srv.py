from socketserver import ThreadingMixIn, TCPServer

class ThreadingTCPSrv(ThreadingMixIn, TCPServer):
    # store dispatch srv conn info 
    dispatch_srv = None
    # trace last conn from dispatch srv
    last_conn = None
    # status
    busy = False
    # liveness
    dead = False