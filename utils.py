import os

from nltk import load_parser

ROOT = os.path.dirname(os.path.abspath(__file__))

GRAMMAR_URL = "file://%(url)s"

# GRAMMAR_DIR = os.path.join(ROOT, 'grammars')

def load_grammar(grammar_file, trace=2, cache=False):
    """ loads a grammar parser from the given grammar file """

    file = GRAMMAR_URL % {'url': os.path.join(ROOT, grammar_file)}
    return load_parser(file, trace=trace, cache=cache)

def go_over_file(file, action):
    """ 
    runs the provided callable on all lines of the provided file 
    """
    
    f = open(file)
    for line in f:
        # remove newline
        actual_line = line[:-1]
        action(actual_line)
    f.close()

