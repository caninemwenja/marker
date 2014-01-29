from .generic import GrammarTest

def test_np():
    grammar = GrammarTest('grammars/test_np.fcfg',
        'grammars/nounphrase.sample', 
        'grammars/nounphrase.sample.negative')
    grammar.check_positive()
    grammar.check_negative()

def test_subject():
    grammar = GrammarTest('grammars/test_subject.fcfg',
        'grammars/subjectphrase.sample',
        'grammars/subjectphrase.sample.negative')
    grammar.check_positive()
    grammar.check_negative()

