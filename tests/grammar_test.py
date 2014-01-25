import nose

from parser_tool import get_parser, parse

sentences = (
    # PN V[i]
    "Brad drives",
    # PN V[t] N[p]
    "Angela drives cars",
    # PN V[t] Det N[s]
    "Brad buys the house",
    # Det[s] N[s] V[i]
    "a dog walks",
    # Det[p] N[p] V[i]
    "these dogs walk",
    # Det[p] N[p] V[t] Det N[s]
    "the cars enter the house",
    # A N[p] V[t] Det N[s]
    "red cars enter the house",
    # Det A N[s] V[t] Det N[s]
    "a red car enters the house",
    # PN V[t] Det A N[s]
    "Brad buys a red car",
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
