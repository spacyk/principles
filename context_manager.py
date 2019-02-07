"""
Example of generic context manager with generator function used on enter and exit.
Simply create before execution and delete table after.

This shows function decorated with context manager.
"""
from sqlite3 import connect
from contextlib import contextmanager


class TemptableContextManager:
    def __init__(self, gen):
        self.gen = gen

    def __call__(self, *args, **kwargs):
        self.args, self.kwargs = args, kwargs
        return self

    def __enter__(self):
        self.gen_inst = self.gen(*self.args, **self.kwargs)
        next(self.gen_inst)

    def __exit__(self, *args):
        next(self.gen_inst, None)


@TemptableContextManager
def temptable(cur):
    cur.execute('create table points(x int, y int)')
    yield
    cur.execute('drop table points')


@contextmanager
def temptable2(cur):
    cur.execute('create table points(x int, y int)')
    yield
    cur.execute('drop table points')

def execute_queries():
    with connect('test.db') as conn:
        cur = conn.cursor()
        # with TemptableContextManager(temptable)(cur):          # One way to do this
        # with temptable(cur):                                   # With own context manager
        with temptable2(cur):                                     # With the builtin contextlib manager
            cur.execute('insert into points (x, y), values(1, 1)')
            for row in cur.execute('select sum(x * y) from points'):
                print(row)
