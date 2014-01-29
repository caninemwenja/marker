import os

from utils import parse_file, get_file_content
from nose import with_setup

test_files = {
    'test1.txt': "some junk\nref test2.txt",
    'test2.txt': "some other junk",
    'test3.txt': "some junk\nsome other junk",
}

def setup():
    for key, value in test_files.iteritems():
        f = open(key, "w")
        f.write(value)
        f.close()

def teardown():
    for key in test_files.keys():
        if os.path.isfile(key):
            os.unlink(key)

@with_setup(setup, teardown)
def test_parse_file():
    content = parse_file('test1.txt')
    control = get_file_content('test3.txt')

    actual_content = "\n".join(content)

    error_msg_tpl = "Content does not match: %s vs %s"
    error_msg = error_msg_tpl % (actual_content, control)
    
    assert actual_content == control, error_msg
