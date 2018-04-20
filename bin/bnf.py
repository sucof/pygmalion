#!/usr/bin/env python3
import sys
import resource
resource.setrlimit(resource.RLIMIT_STACK, [0x10000000, resource.RLIM_INFINITY])
sys.setrecursionlimit(0x100000)
sys.path.append('.')
import os
import pickle
import pygmalion.miner as miner
import pygmalion.refiner as refiner
import pygmalion.util as u
import time
import pudb
brk = pudb.set_trace

if __name__ == "__main__":
    max_sym = int(os.getenv('MAXSYM') or '100')
    nout = int(os.getenv('NOUT') or '100')
    fin = sys.stdin.buffer if len(sys.argv) < 2 else open(sys.argv[1], 'rb')
    fout = sys.stdout if len(sys.argv) < 2 else open("%s.tmp" % sys.argv[1], 'wb')
    grammar = pickle.load(fin)
    print(u.readable_grammar(grammar))