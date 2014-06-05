import sys
import zmq
import logging
from os.path import expanduser, join
from daemon import Daemon

# ToDo: read end points from args
# ToDo: set job status to 'queued'
# ToDo: change to load balancing for workers, not round robin

class JobQueueDaemon(Daemon):
    def run(self):
        print("Starting job queue...")
        context = zmq.Context()
        pull_socket = context.socket(zmq.PULL)
        pull_socket.bind('tcp://127.0.0.1:5000')
        push_socket = context.socket(zmq.PUSH)
        push_socket.bind('tcp://127.0.0.1:5001')

        zmq.device(zmq.FORWARDER, pull_socket, push_socket)

        pull_socket.close()
        push_socket.close()
        context.term()
 
if __name__ == "__main__":
    home = expanduser("~")
    pid_path = join(home, 'daemon-dataunity-job-queue.pid')
    daemon = JobQueueDaemon(pid_path)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)

# if __name__ == '__main__':
#     # ToDo: read end points from args
#     # ToDo: set job status to 'queued'
#     # ToDo: change to load balancing for workers, not round robin
#     print("Starting job queue...")
#     context = zmq.Context()
#     pull_socket = context.socket(zmq.PULL)
#     pull_socket.bind('tcp://127.0.0.1:5000')
#     push_socket = context.socket(zmq.PUSH)
#     push_socket.bind('tcp://127.0.0.1:5001')

#     zmq.device(zmq.FORWARDER, pull_socket, push_socket)

#     pull_socket.close()
#     push_socket.close()
#     context.term()
