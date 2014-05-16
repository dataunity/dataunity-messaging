import sys
import zmq
import logging

if __name__ == '__main__':
    # ToDo: read end points from args
    # ToDo: change to load balancing for workers, not round robin
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
