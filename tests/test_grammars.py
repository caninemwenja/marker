from .generic import GrammarTest

def add_grammar(grammar, positive_sample, negative_sample):
    grammar = GrammarTest(grammar, positive_sample,
        negative_sample)
    grammar.check_positive()
    grammar.check_negative()

def test_np():
    add_grammar('grammars/test_np.fcfg',
        'grammars/nounphrase.sample', 
        'grammars/nounphrase.sample.negative')

def test_subject():
    add_grammar('grammars/test_subject.fcfg',
        'grammars/subjectphrase.sample',
        'grammars/subjectphrase.sample.negative')

def test_object():
    add_grammar('grammars/test_object.fcfg',
        'grammars/object.sample',
        'grammars/object.sample.negative')

def test_prep():
    add_grammar('grammars/test_prep.fcfg',
        'grammars/prep.sample',
        'grammars/prep.sample.negative')
