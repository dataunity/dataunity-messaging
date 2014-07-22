dataunity-messaging
===================

Messaging apps for Data Unity

Install
-------
Checkout git project

Create virtualenv in a suitable location:

<pre>virtualenv no-site-packages env</pre>

Install zeromq
<pre>env/bin/pip install pyzmq</pre>

To run (from root dir):
-----------------------
../env/bin/python jobs/job_queue.py start
../env/bin/python jobs/job_status.py start

To stop (from root dir):
------------------------
../env/bin/python jobs/job_queue.py stop
../env/bin/python jobs/job_status.py stop
