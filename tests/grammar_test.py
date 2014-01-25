import nose

from parser_tool import get_parser, parse

sentences = (
    # N[s] V[i]
    "Brad drives",
    # N[s] V[t] N[p]
    "Angela drives cars",
    # N[s] V[t] Det N[s]
    "Brad buys the house",
    # Det[s] N[s] V[i]
    "a dog walks"
)

grammar = get_parser("grammars/feat1.fcfg", trace=0)

def test_grammar():
    global sentences, parser

    for sent in sentences:
        print "Testing: %s" % sent
        trees = parse(grammar, sent)
        assert len(trees) > 0

if __name__=="__main__":
    nose.main()
