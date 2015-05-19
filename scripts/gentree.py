#!/usr/bin/python

from __future__ import print_function
import sys
sys.path.append('.')

from graph_inference.graphs.tree import TreeGraph

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'n', help='Number of nodes in tree', type=int)
    parser.add_argument(
        'outfile', help='Where to store the generated graph.')
    args = parser.parse_args()

    G = TreeGraph()
    G.generate(n=args.n)
    G.graphml(args.outfile)

if __name__ == '__main__':
    main()
