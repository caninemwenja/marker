# parser.py - parses a given sentence using a given grammar definition

import sys, os
import argparse

from utils import load_grammar

def get_parser(grammar_file, *args, **kwargs):
    """ loads a parser from the given grammar """
    return load_grammar(grammar_file, *args, **kwargs)

def tokenize(sentence):
    """ breaks down a string into tokens for parsing """

    return sentence.split()

def parse(parser, sentence):
    """ gets the best parse trees for this sentence """

    return parser.nbest_parse(tokenize(sentence))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('grammar', 
        help="file in local folder with grammar")
    parser.add_argument('sentence', nargs="*",
        help="sentence to be parsed")
    parser.add_argument('-t', '--trace', type=int, 
        help="parser debug trace level")
    parser.add_argument('-c', '--cache', action="store_true",
        help="cache grammar or not")
    parser.add_argument('-f', '--feature',
        help="show feature in parse tree")

    args = parser.parse_args()

    sentence = " ".join(args.sentence)

    parser = get_parser(args.grammar, trace=args.trace, cache=args.cache)
    trees = parse(parser, sentence)

    if len(trees) == 0:
        print "No parse trees found"
        return

    for tree in trees:
        print tree
        if args.feature and args.feature in tree.node:
            print tree.node[args.feature]

if __name__ == "__main__":
    main()
