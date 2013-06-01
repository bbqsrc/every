from simplebdd import Description, Test, async
from every import run

import time

def stub():
    pass

class Context:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

class EveryTests(Test):
    class RunMethod(Description):
        """Test run() functionality"""

        @async
        def it_should_stop_quickly(self):
            """It should stop quickly"""
            ts = time.time()
            x = run(stub).every(1, 'days')
            x.join()
            ts = time.time() - ts

            # Should end within 3 seconds
            return ts < 3

        @async
        def it_should_run_every_5_seconds(self):
            """It should run every 2 seconds"""
            ctx = Context()
            x = run(ctx.increment).every(2, 'seconds')
            time.sleep(9)
            x.join()
            return ctx.count == 5

        @async
        def it_should_run_immediately(self):
            """It should run immediately"""
            ctx = Context()
            x = run(ctx.increment).every(1, 'hours')
            x.join()
            return ctx.count == 1

        @async
        def it_should_not_run_immediately(self):
            """It should not run immediately"""
            ctx = Context()
            x = run(ctx.increment).every(1, 'hours', immediate=False)
            x.join()
            return ctx.count == 0

        @async
        def it_should_run_once(self):
            ctx = Context()
            x = run(ctx.increment).every(3, 'seconds')
            x.join()
            return ctx.count == 1

        @async
        def it_should_run_twice(self):
            ctx = Context()
            x = run(ctx.increment).every(3, 'seconds')
            x.join(stop=False)
            return ctx.count == 2

