from parser_tool import parse, get_parser
from utils import go_over_file

grammar = get_parser("grammars/test_np.fcfg", trace=0)

def test_np_positive():
    def is_ok(sentence):
        trees = parse(grammar, sentence)
        assert len(trees) > 0, "Failed Positive: %s" % sentence
    
    go_over_file("grammars/nounphrase.sample", is_ok)

def test_np_negative():
    """ tests to see if grammar refuses wrong samples """
    
    def is_not_ok(sentence):
        trees = parse(grammar, sentence)
        assert len(trees) == 0, "Failed Negative: %s" % sentence

    go_over_file("grammars/nounphrase.sample.negative", is_not_ok)

