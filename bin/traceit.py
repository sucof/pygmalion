#!/usr/bin/env python3
import sys
sys.path.append('.')
import resource
resource.setrlimit(resource.RLIMIT_STACK, [0x10000000, resource.RLIM_INFINITY])
sys.setrecursionlimit(0x100000)

import taintedstr
import sys
import os.path
import pygmalion.ftrace as tracer
import pickle
import imp
from contextlib import contextmanager


def records(f):
    try:
        while not f.closed:
            yield pickle.load(f)
    except EOFError:
        raise StopIteration

@contextmanager
def opened_file(f):
    if not f:
        yield sys.stdout.buffer
    else:
        with open(f, 'wb') as f:
            yield f

if __name__ == "__main__":
    m_file = sys.argv[1]
    mod_obj = imp.new_module('example')
    mod_obj.__file__ = m_file
    code = compile(open(m_file).read(), os.path.basename(m_file), 'exec')
    exec(code, mod_obj.__dict__)
    if len(sys.argv) > 2:
        fn = sys.argv[2]
        inp = sys.argv[3]
    else:
        fn = None
        inp = None
    with opened_file(fn) as trace_file:
        with opened_file(inp) as myinput:
            # Infer grammar
            for j,(t,_i) in enumerate(records(inp)):
                i = taintedstr.tstr(i)
                print("trace:",j, repr(i), file=sys.stderr)
                with tracer.Tracer(i, trace_file) as t:
                    t._my_files = ['%s' % os.path.basename(m_file)]
                    t._skip_classes = mod_obj.skip_classes() if hasattr(mod_obj, 'skip_classes') else []
                    o = mod_obj.main(i)
