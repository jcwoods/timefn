import atexit
import time

class TimeCollector(object):
    '''
    Only one TimeCollector object (a singleton).  This class tracks all of
    the FunctionTimeAccumulator objects allocated during the run.
    '''

    instance = None

    class __InnerTimeCollector(object):
        def __init__(self):
            self.tracked_functions = []    # list of FTA objects
            atexit.register(self.report)   # make sure we dump stats last.

        def report(self):
            for tao in TimeCollector.instance.tracked_functions:
                tao.show_report()
            return

    def __init__(self):
        if TimeCollector.instance is None:
            TimeCollector.instance = TimeCollector.__InnerTimeCollector()
    
    def add_accumulator(self, fta):
        '''
        Add the given FunctionTimeAccumulator to the TimeCollector
        '''

        TimeCollector.instance.tracked_functions.append(fta)

    def report(self):
        '''
        Generate a report for each FunctionTimeAccumulator.
        '''

        TimeCollector.instance.report()
        return

class FunctionTimeAccumulator(object):
    def __init__(self, fn):
        self.func = fn
        self.count = 0
        self.timings = []

    def show_report(self):
        n = 0
        total = 0.0
        min_val = None
        max_val = None
        min_pos = None
        max_pos = None

        for t in self.timings:
            if min_val is None or t < min_val:
                min_val = t
                min_pos = n

            if max_val is None or t > max_val:
                max_val = t
                max_pos = n

            total += t
            n += 1

        print("")
        print("Report for: " + self.func.__name__)
        print("    times called:  {0:8d}".format(n))

        if n == 0:
            return

        average = total / n
        min_pos = min_pos
        max_pos = max_pos

        print("    min value:     {0:3.6f} [{1:d}]".format(min_val, min_pos))
        print("    max value:     {0:3.6f} [{1:d}]".format(max_val, max_pos))
        print("    avg value:     {0:3.6f}".format(average))

        return

    def __call__(self, *args, **kwargs):
        st = time.time()
        result =  self.func(*args, **kwargs)
        et = time.time() - st

        self.timings.append(et)
        self.count += 1
        return result
            
def timefn(fn):
    '''
    This is the annotation used to mark functions for tracking.  For example,
    
    @timereport
    def myadder(a, b):
        return a + b

    The report will be displayed when the process is shutting down (atexit).
    '''

    tc = TimeCollector()
    fta = FunctionTimeAccumulator(fn)
    tc.add_accumulator(fta)

    return fta

'''
Example usage:

@timefn
def doadd(a, b):
    return a + b

@timefn
def dosub(a, b):
    return a - b

for i in range(1, 100):
    doadd(i, i+1)

for i in range(1, 100):
    dosub(i, i+1)
'''
