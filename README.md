# Socketeer: A multi-threaded, fault-tolerant task-runner for continuous integration

## Usage

## Architecture

Socketeer observes a target git repository for commit SHA changes. When the main branch's HEAD changes, a message is broadcast to all deployments (task-runners), which then execute a series of pre-defined tasks. The runners then report the results of these tasks back to the dispatcher.

![Architecture Control Flow](https://github.com/MatthewZito/socketeer/blob/master/docs/socketeer.png)

### Observer

The observer component polls the target repository, notifying a dispatch service of new commit SHAs. 

### Dispatch Srv

The dispatch service delegates tasks. It listens for requests for task-runners from the observer. This service is also responsible for monitoring the health of all threads - if a task-runner process dies, or prematurely exits, the remaining task pool is redistributed to the available threads. If no threads are available, the dispatch service will spawn them.

### Task-runners & Jobs

The redistribution and task-runner monitor each run on their own dedicated threads, for which the dispatcher provides failover redundancy.

The task-runner monitor pings each registered task runner to ensure liveness. If a runner has become unresponsive - and what constitutes as 'responsive' here is a configurable timeout period - the runner is removed from the pool and its task ID is reassigned to the next available thread. 

The redistributor thread polls the tasks pool for new commit SHAs and assigns new work as needed.

## Threaded Socket Server

Python's SocketServer TCPServer out-of-the-box can only handle a single request at any given time. If the dispatch service needs to talk to more than one task-runner, for example, using this default would mean synchronous, blocking I/O.

In its stead, Socketeer uses a modified socket server that handles threading; a new process is spawned for each inbound connection.
