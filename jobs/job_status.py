import sys
import zmq
import logging
import time

# ToDo: replace this hack with lookup in Redis
job_status = {}

if __name__ == '__main__':
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
            # process task
            print(str(message))

        if status_request_reply in socks:
            message = status_request_reply.recv()
            print(message)
            status_request_reply.send("Hello")

#    while True:
#
#        # Process any waiting tasks
#        while True:
#            
#
#            try:
#                status_update_msg = status_request_reply.recv(zmq.DONTWAIT)
#                print(status_update_msg)
#                status_request_reply.send("Hello")
#            except zmq.Again:
#                break
#            # process task

#            # ToDo: updates should probably have priority, but 
#            # causes status to hang - check out
#            try:
#                msg = status_update.recv(zmq.DONTWAIT)
#                print(str(msg))
#            except zmq.Again:
#                break
#            # process task
            

        # No activity, so sleep for 1 msec
        time.sleep(0.001)

    status_update.close()
    status_request_reply.close()
    context.term()
