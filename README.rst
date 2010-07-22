---------
Job_Queue
---------

This is an answer to the fact that Pool() isn't working how I need it to for a
project. So I made a super simple running queue, that has a bubble of
execution.


Requires
--------

python 2.5 with 3rd party install or >2.6, and the mutltiprocessing module, as 
it takes Process()es as its queue members.


Brief explination
-----------------
The goal of this class is to make a queue of processes to run, and go through 
them running X number at any given time. 

So if the bubble is 5 start with 5 running and move the bubble of running procs
along the queue looking something like this:

    ---------------------------
    [-----]--------------------
    ---[-----]-----------------
    ---------[-----]-----------
    ------------------[-----]--
    --------------------[-----]
    ---------------------------


Contact
-------

Github messages are fine, username goosemo. But best way to reach me is via
email at morgan.goose@gmail.com

I welcome suggestions, and bug reports.


