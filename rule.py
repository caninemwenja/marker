import argparse

RULE_TEMPLATE = "%(lhd)s -> %(rhd)s"

def rule(args):
    rhd = args.RHD

    if args.terminal:
        rhd = map(lambda x: "'"+x+"'", rhd)
    
    helper_dict = { 'lhd' : args.LHD, 'rhd': " | ".join(rhd)}
    print RULE_TEMPLATE % helper_dict

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("LHD",
        help="left hand side of rule")
    parser.add_argument("RHD", nargs="*",
        help="right hand side of rule")

    parser.add_argument('-t', '--terminal', action="store_true",
        help="adds quotes around terminal productions")
    
    args = parser.parse_args()
    rule(args)

if __name__ == "__main__":
    main()
