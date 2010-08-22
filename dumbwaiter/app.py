import sched
import threading
import time
import types
from django.utils import importlib
from dumbwaiter import app_settings
from dumbwaiter.models import CachedResult, ErrorReport

class Dumbwaiter(object):
    def __init__(self, functions=None):
        if functions is None:
            functions = app_settings.FUNCTION_LIST

        self.functions = []

        for fn in functions:
            self.functions.append(DumbwaiterFunction(**fn))

    def run(self):
        if app_settings.THREADED:
            self.run_threaded()
        else:
            self.run_unthreaded()

    def run_threaded(self):
        threads = []
        try:
            for fn in self.functions:
                t = DumbwaiterThread(function=fn)
                t.start()
                threads.append(t)
            while True:
                time.sleep(10000)
        finally:
            for t in threads:
                t.keep_running = False

    def run_unthreaded(self):
        s = sched.scheduler(time.time, time.sleep)
        def reschedule(self):
            s.enter(self.frequency, 1, self, [])
        for fn in self.functions:
            fn.reschedule = types.MethodType(reschedule, fn, DumbwaiterFunction)
        while True:
            try:
                s.run()
            except Exception:
                pass
            else:
                if s.empty():
                    for fn in self.functions:
                        fn.reschedule()

class DumbwaiterThread(threading.Thread):
    def __init__(self, function):
        self.function = function
        self.keep_running = True
        threading.Thread.__init__(self)
        self.daemon = True

    def run(self):
        while self.keep_running:
            self.function() # The function will clean up its own errors and exceptions
            time.sleep(self.function.frequency)

class DumbwaiterFunction(object):
    def __init__(self, function, name, frequency=app_settings.DEFAULT_FREQUENCY, args=[], kwargs={}, max_saved=app_settings.MAX_SAVED, reschedule=None):
        self.name = name
        self.frequency = frequency
        self.args = list(args)
        self.kwargs = dict(kwargs)
        self.max_saved = max_saved
        self.reschedule = reschedule

        if isinstance(function, basestring):
            try:
                fn_base, fn_name = function.rsplit(".", 1)
                self.function = getattr(importlib.import_module(fn_base), fn_name)
            except:
                raise ImportError("Unable to import Dumbwaiter function %s" % function)
        else:
            self.function = function

    def __call__(self):
        return self.run()

    def run(self):
        try:
            data = self.function(*self.args, **self.kwargs)
            result = CachedResult(name=self.name, data=data)
            result.save()
            CachedResult.objects.limit_to(name=self.name, number=self.max_saved)
        except Exception, e:
            report = ErrorReport(name=self.name, log=unicode(e))
            report.save()
            ErrorReport.objects.limit_to(name=self.name, number=self.max_saved)
        finally:
            if self.reschedule:
                print "Rescheduling %s" % self.name
                self.reschedule()
