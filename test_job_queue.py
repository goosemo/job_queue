import sys 
from nose.tools import *
from job_queue import Job_Queue, try_using
from cStringIO import StringIO


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout

class Test_Job_Queue():

    from multiprocessing import Process as Bucket

    def test_init(self):
        jobs = Job_Queue(5)
        assert_equal(jobs._queued, [])
        assert_equal(jobs._running, [])
        assert_equal(jobs._completed, [])
        assert_equal(jobs._num_of_jobs, 0)
        assert_equal(jobs._max, 5)
        assert_false(jobs._finished)
        assert_false(jobs._closed)
        assert_false(jobs._debug)
        jobs._debug = True
        assert_true(jobs._debug)


    def populate(self,queue_size=5,job_size=10,debug=False):
        jobs = Job_Queue(queue_size)
        jobs._debug = debug
     
        def foo():
            return 10
     
        for x in range(job_size):
            jobs.append(self.Bucket(
                target = foo, 
                args = [],
                kwargs = {},
                ))

        return jobs

    def test_empty(self):
	"""This case is when less jobs than the size of the queue are added
	"""
        jobs = self.populate(2,1)
        jobs.close()
        jobs.start()

    @raises(Exception)
    def test_some(self):
        jobs = self.populate()
        jobs.start()


    def test_length(self):
        jobs = self.populate()
        assert_equal( jobs._num_of_jobs, 10)
        assert_equal( len(jobs._queued), 10)
        assert_equal(len(jobs), 10)


    def test_closed(self):
        jobs = self.populate()
        assert_false(jobs._closed)
        jobs.close()
        assert_true(jobs._closed)


    def test_runs(self):
        jobs = self.populate()
        jobs.close()
        assert_false(jobs._finished)
        jobs.start()
        assert_true(jobs._finished)
        assert_false(jobs._all_alive())
        assert_equal(jobs._running,[])

    def test_runs_debug(self):
        with Capturing() as output:
            jobs = self.populate(debug=True)
            jobs.close()
            assert_false(jobs._finished)
            jobs.start()
            assert_true(jobs._finished)
            assert_false(jobs._all_alive())
            assert_equal(jobs._running,[])

        assert_true(len(output)>0)

    def test_runs_try_using(self):
        try_using("multiprocessing")
        try_using("threading")

class Test_Job_Queue_Threads(Test_Job_Queue):

    from threading import Thread as Bucket
