import os

from nose import with_setup

from ..utils import parse_file, get_file_content

test_files = {
    'test1.txt': "some junk\nref test2.txt",
    'test2.txt': "some other junk",
    'test3.txt': "some junk\nsome other junk",
    'test4.txt': "junk\nref test1.txt\nref test2.txt",
    'test5.txt': "junk\nsome junk\nsome other junk",
    'test6.txt': "junk\n#comment",
    'test7.txt': "junk",
}

error_msg_tpl = "Content does not match: %s vs %s"

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

    error_msg = error_msg_tpl % (actual_content, control)    
    assert actual_content == control, error_msg

@with_setup(setup, teardown)
def test_circular_ref():
    content = parse_file('test4.txt')
    actual_content = "\n".join(content)

    control = get_file_content('test5.txt')

    error_msg = error_msg_tpl % (actual_content, control)
    assert actual_content == control, error_msg

@with_setup(setup, teardown)
def test_ignore_lines():
    ignore_lines = [
        "^\#.*",
    ]
    content = parse_file('test6.txt', ignore_lines=ignore_lines)
    actual_content = "\n".join(content)

    control = get_file_content('test7.txt')

    error_msg = error_msg_tpl % (actual_content, control)
    assert actual_content == control, error_msg

