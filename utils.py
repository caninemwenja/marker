import os, re
import tempfile

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
    except IOError, e:
        raise Exception("Missing reference file: %s" % str(e))

def clean_lines(data):
    lines = data.split("\n")

    # get rid of the newline
    lines = map(lambda x: x.replace('\n',''), lines)

    return lines

def get_file_lines(filename):
    return clean_lines(get_file_content(filename))

def parse_file(filename, seen_ref=None, ignore_lines=None):
    """ 
    builds a large file from references to other files
    """

    content = []
    seen_ref = seen_ref or []
    
    ignore_compiler=None

    if ignore_lines:
        ignore_regex = "|".join(ignore_lines)
        ignore_compiler = re.compile(ignore_regex)

    lines = get_file_lines(filename)

    for line in lines:
        if ignore_compiler and ignore_compiler.match(line):
                continue

        match = REF_REGX_COMPILER.match(line)
        if match:
            url = match.group('url')

            # watch out for circular references
            if url not in seen_ref:
                seen_ref.append(url)
                content += parse_file(match.group('url'), 
                    seen_ref, ignore_lines)
        else:
            content.append(line)

    return content

def load_file(filename):
    ignore_lines = [
        "^\#.*$", # ignore comments
    ]
    content = parse_file(filename)
    actual_content = "\n".join(content)
    return actual_content

def load_grammar(grammar_file, trace=2, cache=False):
    """ loads a grammar parser from the given grammar file """

    # get grammar extension to pass to temp file name
    ext = os.path.splitext(grammar_file)[-1]

    # make temp file from ref parsed files and pass it load_parse
    temp_file, temp_file_path = tempfile.mkstemp(suffix=ext,text=True)

    temp_file = open(temp_file_path, "w")
    temp_file.write(load_file(grammar_file))
    temp_file.close()

    file = GRAMMAR_URL % {'url': os.path.join(ROOT, temp_file_path)}
    parser = load_parser(file, trace=trace, cache=cache)

    # cheekily remove temp file
    os.unlink(temp_file_path)

    return parser

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

