# parser.py - parses a given sentence using a given grammar definition

import sys, os

from nltk import load_parser

ROOT = os.path.dirname(os.path.abspath(__file__))

GRAMMAR_URL = "file://%(url)s"

# GRAMMAR_DIR = os.path.join(ROOT, 'grammars')

USAGE = "Usage: %(prog)s grammar-file sentence trace cache"

def get_parser(grammar_file, trace=2, cache=False):
    """ loads a parser from the given grammar """

    file = GRAMMAR_URL % {'url': os.path.join(ROOT, grammar_file)}
    return load_parser(file, trace=trace, cache=cache)

def tokenize(sentence):
    """ breaks down a string into tokens for parsing """

    return sentence.split()

def parse(parser, sentence):
    """ gets the best parse trees for this sentence """

    return parser.nbest_parse(tokenize(sentence))

def main():
    if len(sys.argv) < 3:
        print USAGE % sys.argv[0]

    grammar_file = sys.argv[1]
    sentence = sys.argv[2]

    trace = 0
    cache = False

    if len(sys.argv) > 3:
        trace = int(sys.argv[3])

    if len(sys.argv) > 4 and sys.argv[4] == "True":
        cache = True

    parser = get_parser(grammar_file, trace=trace, cache=cache)
    trees = parse(parser, sentence)

    if len(trees) == 0:
        print "No parse trees found"
        return

    for tree in trees:
        print tree

if __name__ == "__main__":
    main()
