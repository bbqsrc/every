import time
from threading import Thread


class Every(Thread):
    def __init__(self, *args, **kwargs):
        Thread.__init__(self, *args, **kwargs)
        self._repr_amt = None
        self.period = None
        self.joined = False

    def run(self, *args, **kwargs):
        if self._target is None:
            return

        immediate = self.immediate

        while self.looping:
            future = time.time() + self.amount
            try:
                if not immediate:
                    immediate = True
                else:
                    self._target(*self._args, **self._kwargs)
                if self.joined:
                    break
            finally:
                while future > time.time():
                    if self.looping and not self.joined:
                        time.sleep(1)
                    else:
                        break

    def every(self, amount, period="seconds", immediate=True):
        self._repr_amt = amount

        if period == "seconds":
            pass
        elif period == "minutes":
            amount *= 60
        elif period == "hours":
            amount *= 60 * 60
        elif period == "days":
            amount *= 60 * 60 * 24
        else:
            raise Exception("invalid period")

        self.amount = amount
        self.period = period
        self.looping = True
        self.immediate = immediate
        self.start()
        return self

    def join(self, timeout=None, stop=True):
        self.joined = True
        self.looping = not stop
        return Thread.join(self, timeout)

    def __repr__(self):
        assert self._initialized, "Thread.__init__() was not called"
        status = "initial"
        if self._started.is_set():
            status = "started"
        if self._stopped:
            status = "stopped"
        if self._daemonic:
            status += " daemon"
        if self._ident is not None:
            status += " %s" % self._ident
        if self._repr_amt and self.period:
            status += ", every %s %s" % (self._repr_amt, self.period)

        return "<%s (%s, %s)>" % (self.__class__.__name__, self._name, status)


def run(method, *args, **kwargs):
    return Every(target=method, args=args, kwargs=kwargs)
