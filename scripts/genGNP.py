from __future__ import print_function

from graph_inference.graphs.gnp import GNPgraph

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'n', help='Number of nodes in graph', type=int)
    parser.add_argument(
        'p', help='Edge existence probability', type=float)
    parser.add_argument(
        'outfile', help='Where to store the generated graph.')
    args = parser.parse_args()

    print('n:', args.n, 'p:', args.p)

if __name__ == '__main__':
    main()
