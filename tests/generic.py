from ..parser_tool import parse, get_parser
from ..utils import go_over_file

class GrammarTest(object):
    
    def __init__(self, grammar, positive, negative):
        self.grammar = grammar
        self.positive = positive
        self.negative = negative

        self.parser = get_parser(self.grammar, trace=0)
    
    def trees(self, sentence):
        return parse(self.parser, sentence)

    def is_ok(self, sentence):
        assert len(self.trees(sentence)) > 0, \
            "Failed Positive: %s" % sentence

    def is_not_ok(self, sentence):
        assert len(self.trees(sentence)) == 0, \
            "Failed negative: %s" % sentence

    def check_positive(self):
        go_over_file(self.positive, self.is_ok)

    def check_negative(self):
        go_over_file(self.negative, self.is_not_ok)


