import os, re

from nltk import load_parser

ROOT = os.path.dirname(os.path.abspath(__file__))

GRAMMAR_URL = "file://%(url)s"

# GRAMMAR_DIR = os.path.join(ROOT, 'grammars')

REF_PATTERN = "^ref (?P<url>.*(\/.*)*)$"

REF_REGX_COMPILER = re.compile(REF_PATTERN)

def get_file_content(filename):
    try:
        f = open(filename)
        data = f.read()
        f.close()

        return data
    except IOError:
        raise Exception("Missing reference file")

def clean_lines(data):
    lines = data.split("\n")

    # get rid of the newline
    lines = map(lambda x: x.replace('\n',''), lines)

    return lines

def get_file_lines(filename):
    return clean_lines(get_file_content(filename))

def parse_file(filename):
    """ 
    builds a large file from references to other files
    """

    content = []

    lines = get_file_lines(filename)

    for line in lines:
        match = REF_REGX_COMPILER.match(line)
        if match:
            content += parse_file(match.group('url'))
        else:
            content.append(line)

    return content

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

