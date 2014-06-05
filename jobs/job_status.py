import sys
import zmq
import logging
import time
import json
from os.path import expanduser, join
from daemon import Daemon

# ToDo: replace this hack with lookup in Redis
job_status = {}

def parse_job_msg(msg):
    """Parses a job message received from message queue.

    :param msg: The message from the queue
    :type msg: string
    :returns: Dict of message values
    :rtype: dict"""
    return json.loads(msg)

class JobStatusDaemon(Daemon):
    def run(self):
        # ToDo: read end points from args
        print("Starting job status tracker...")
        context = zmq.Context()
        status_update = context.socket(zmq.PULL)
        status_update.connect("tcp://127.0.0.1:5002")
        status_request_reply = context.socket(zmq.REP)
        status_request_reply.bind("tcp://127.0.0.1:5003")

        poller = zmq.Poller()
        poller.register(status_update, zmq.POLLIN)
        poller.register(status_request_reply, zmq.POLLIN)

        while True:
            try:
                socks = dict(poller.poll())
            except KeyboardInterrupt:
                break

            if status_update in socks:
                message = status_update.recv()
                # Update job status
                #print(str(message))
                msg_data = parse_job_msg(message)
                about = msg_data.get("about")
                if about is None:
                    raise KeyError("Expected message to contain 'about' to identify resource.")
                job_status[about] = msg_data
                #print(msg_data['data'])

            if status_request_reply in socks:
                message = status_request_reply.recv()
                #print(message)
                # Update caller about job status
                msg_data = parse_job_msg(message)
                about = msg_data.get("about")
                if about is None:
                    raise KeyError("Expected message to contain 'about' to identify resource.")
                job_status_data = job_status.get(about)
                print("Replying with job status.")
                status_request_reply.send(json.dumps(job_status_data))

            # No activity, so sleep for 1 msec
            time.sleep(0.001)

        status_update.close()
        status_request_reply.close()
        context.term()



if __name__ == "__main__":
    home = expanduser("~")
    pid_path = join(home, 'daemon-dataunity-job-status.pid')
    daemon = JobStatusDaemon(pid_path)
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
#     print("Starting job status tracker...")
#     context = zmq.Context()
#     status_update = context.socket(zmq.PULL)
#     status_update.connect("tcp://127.0.0.1:5002")
#     status_request_reply = context.socket(zmq.REP)
#     status_request_reply.bind("tcp://127.0.0.1:5003")

#     poller = zmq.Poller()
#     poller.register(status_update, zmq.POLLIN)
#     poller.register(status_request_reply, zmq.POLLIN)

#     while True:
#         try:
#             socks = dict(poller.poll())
#         except KeyboardInterrupt:
#             break

#         if status_update in socks:
#             message = status_update.recv()
#             # Update job status
#             #print(str(message))
#             msg_data = parse_job_msg(message)
#             about = msg_data.get("about")
#             if about is None:
#                 raise KeyError("Expected message to contain 'about' to identify resource.")
#             job_status[about] = msg_data
#             #print(msg_data['data'])

#         if status_request_reply in socks:
#             message = status_request_reply.recv()
#             #print(message)
#             # Update caller about job status
#             msg_data = parse_job_msg(message)
#             about = msg_data.get("about")
#             if about is None:
#                 raise KeyError("Expected message to contain 'about' to identify resource.")
#             job_status_data = job_status.get(about)
#             print("Replying with job status.")
#             status_request_reply.send(json.dumps(job_status_data))

#         # No activity, so sleep for 1 msec
#         time.sleep(0.001)

#     status_update.close()
#     status_request_reply.close()
#     context.term()
