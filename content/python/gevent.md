Title: Gevent Internals
Date: 2014-09-23 14:00
Summary: How gevent works

#Introduction

[Gevent][gevent] is an efficient coroutine-based asynchronous concurrency framework, it is based on [libev][libev] and [greenlet][greenlet].
If you don't know how [greenlet][greenlet] works, recommend to read [this](http://www.slideshare.net/saghul/understanding-greenlet). If you only want to know how to use gevent, recommend you read <http://sdiehl.github.io/gevent-tutorial/>.

#Greenlet diagram

First an example from official website. 

    >>> import gevent
    >>> from gevent import socket
    >>> urls = ['www.google.com', 'www.example.com', 'www.python.org']
    >>> jobs = [gevent.spawn(socket.gethostbyname, url) for url in urls]
    >>> gevent.joinall(jobs, timeout=2)
    >>> [job.value for job in jobs]
    ['74.125.79.106', '208.77.188.166', '82.94.164.162']

In this example gevent retrieve three ips from web concurrently.
`jobs = [gevent.spawn(socket.gethostbyname, url) for url in urls]` create three task greenlets, and
`gevent.joinall(jobs, timeout=2)` wait all the three task greenlets finished.

This is the greenlet diagram of the program.

                                 +-----+
                          +----> | task|
                          |      +-----+
                          |            
    +-------+      +-----++      +-----+
    | main  +----> | hub |-----> | task|
    +-------+      +-----++      +-----+
                          |            
                          |      +-----+
                          +----> | task|
                                 +-----+


# How it works

`main` is the default greenlet, `task` is the greenlet that do the real job, `hub` greenlet is the core of gevent, it cooperates all other greenlets, including `main`.
So what is `hub`? `hub` is where gevent use [libev][libev]. When [gevent][gevent] initializes, it create `hub` first, and `hub` is singleton, only one `hub` exists in the thread.

    :::python
    def get_hub(*args, **kwargs):
        """Return the hub for the current thread.

        If hub does not exists in the current thread, the new one is created with call to :meth:`get_hub_class`.
        """
        global _threadlocal
        try:
            return _threadlocal.hub
        except AttributeError:
            hubtype = get_hub_class()
            hub = _threadlocal.hub = hubtype(*args, **kwargs)
            return hub

When use do `gevent.spawn`, gevent will create a task greenlet using `hub` as parent.

    :::python
    spawn = Greenlet.spawn

    class Greenlet(greenlet):
        """A light-weight cooperatively-scheduled execution unit."""

        def __init__(self, run=None, *args, **kwargs):
            hub = get_hub()
            greenlet.__init__(self, parent=hub)

        def start(self):
            """Schedule the greenlet to run in this loop iteration"""
            self._start_event = self.parent.loop.run_callback(self.switch)

        @classmethod
        def spawn(cls, *args, **kwargs):
            """Return a new :class:`Greenlet` object, scheduled to start.

            The arguments are passed to :meth:`Greenlet.__init__`.
            """
            g = cls(*args, **kwargs)
            g.start()
            return g


At the begining, we said [gevent][gevent] use [libev][libev], here `self.parent.loop.run_callback(self.switch)`, `loop` is from [libev][libev], we register the new created task greenlet to `loop`. when the `loop` runs, it will execute the task greenlet.

So when `loop` runs, when `main` do some block operations, it will switch to `hub`,

    :::python
    def run(self):
        assert self is getcurrent(), 'Do not call Hub.run() directly'
        while True:
            loop = self.loop
            loop.error_handler = self
            try:
                loop.run()
            finally:
                loop.error_handler = None  # break the refcount cycle
            self.parent.throw(LoopExit('This operation would block forever'))

`loop.run()` will be executed, so `loop` can choose one greenlet to run, when the greenlet is also block or finished, it will choose another one to run.

Next explain monkeypatch

# Ref

<http://blog.segmentfault.com/fantix/1190000000613814>

<https://github.com/surfly/gevent>

[gevent]: http://www.gevent.org/
[greenlet]: http://greenlet.readthedocs.org/en/latest/
[libev]: http://software.schmorp.de/pkg/libev.html
