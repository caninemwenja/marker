from parser_tool import parse, get_parser

def test_np():
    grammar = get_parser("grammars/test_np.fcfg", trace=0)

    f = open("grammars/nounphrase.sample")
    for line in f:
        # remove newline
        actual_line = line[:-1]

        trees = parse(grammar, actual_line)
        assert len(trees) > 0, "Failed: %s" % actual_line
    f.close()
