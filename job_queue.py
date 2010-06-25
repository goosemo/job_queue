

class Job_Queue(object):

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
        return all([x.is_alive() for x in self._running])

    def close(self):
        if self._debug:
            print("job queue closed.")

        self._num_of_jobs = len(self._queued)
        self._closed = True

    def append(self, process):
        if not self._closed:
            if self._debug:
                print("job queue appended to.")
            self._queued.append(process)

    def start(self):
        if not self._closed:
            raise Exception("Need to close() before starting.")

        if self._debug:
            print("job queue starting.")

        while len(self._running) < self._max:
            if self._debug:
                print("job queue intial running queue fill.")

                job = self._queued.pop()
                job.start()
                self._running.append(job)

        while not self._finished:

            while len(self._running) < self._max:
                if self._debug:
                    print("job queue running queue filling.")

                job = self._queued.pop()
                job.start()
                self._running.append(job)


            if not self._all_alive():
                for id, job in enumerate(self._running):
                    if not job.is_alive():
                        if self._debug:
                            print("job queue found finished proc.")

                        done = self._running.pop(id)
                        self._completed.append(done)

            if self._debug:
                print("job queue has %d running." % len(self._running))

            if not (self._queued and self._running): #and 
                #len(self._completed) == self._num_of_jobs):
                if self._debug:
                    print("job queue finished.")

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
