

class Job_Queue(object):
    """
    The goal of this class is to make a queue of processes to run, and go
    through them running X number at any given time. 

    So if the bubble is 5 start with 5 running and move the bubble of running
    procs along the queue looking something like this:

    ---------------------------
    [-----]--------------------
    ---[-----]-----------------
    ---------[-----]-----------
    ------------------[-----]--
    --------------------[-----]
    ---------------------------
    """

    def __init__(self, max_running):
        self._queued = []
        self._running = []
        self._completed = []
        self._num_of_jobs = 0
        self._max = max_running
        self._finished = False
        self._closed = False
        self._debug = False

    def _all_alive(self):
        """
        Simply states if all procs are alive or not. Needed to determine when
        to stop looping, and pop dead procs off and add live ones.
        """
        return all([x.is_alive() for x in self._running])

    def close(self):
        """
        A sanity check, so that the need to care about new jobs being added in
        the last throws of the job_queue's run are negated.
        """
        if self._debug:
            print("job queue closed.")

        self._num_of_jobs = len(self._queued)
        self._closed = True

    def append(self, process):
        """
        Add the Process() to the queue, so that later it can be checked up on.
        That is if the Job_Queue is still open.
        """
        if not self._closed:
            self._queued.append(process)
            if self._debug:
                print("job queue appended %s." % process.name)

    def start(self):
        """
        This is the workhorse. It will take the intial jobs from the _queue,
        start them, add them to _running, and then go into the main running
        loop.

        This loop will check for done procs, if found, move them out of
        _running into _completed. It also checks for a _running queue with open
        spots, which it will then fill as discovered.

        To end the loop, there have to be no running procs, and no more procs
        to be run in the queue.

        When all if finished, it will exit the loop, and disconnect_all()
        """

        def _advance_the_queue():
            """
            Helper function to do the job of poping a new proc off the queue
            start it, then add it to the running queue. This will eventually
            depleate the _queue, which is a condition of stopping the running
            while loop.
            """
            job = self._queued.pop()
            job.start()
            self._running.append(job)

        if not self._closed:
            raise Exception("Need to close() before starting.")

        if self._debug:
            print("Job queue starting.")
            print("Job queue intial running queue fill.")

        while len(self._running) < self._max:
            _advance_the_queue()

        while not self._finished:

            while len(self._running) < self._max and self._queued:
                if self._debug:
                    print("Job queue running queue filling.")
              
                _advance_the_queue()

            if not self._all_alive():
                for id, job in enumerate(self._running):
                    if not job.is_alive():
                        if self._debug:
                            print("Job queue found finished proc: %s." %
                                    job.name)

                        done = self._running.pop(id)
                        self._completed.append(done)

                if self._debug:
                    print("Job queue has %d running." % len(self._running))

            if not (self._queued or self._running):
                if self._debug:
                    print("Job queue finished.")

                for job in self._completed:
                    job.join()

                self._finished = True


def test_Job_Queue():

    def print_number(number):
        print(number)

    from multiprocessing import Process

    jobs = Job_Queue(5)
    jobs._debug = True

    for x in range(20):
        jobs.append(Process(
            target = print_number,
            args = [x],
            kwargs = [],
            ))

    jobs.close()
    jobs.start()


if __name__ == '__main__':
    test_Job_Queue()
