import argparse

from pattern.en import pluralize
from nltk.corpus import wordnet as wn

def wn_browse(pos, action):
    for i in wn.all_synsets(pos):
        action(i)

def synset_name(synset):
    return synset.name.split(".")[0]

def print_tag(synset):
    print synset_name(synset)

def gen_nouns(args):
    def print_plural(synset):
        print pluralize(synset_name(synset))
    
    def print_combined(synset):
        print_tag(synset)
        print_plural(synset)
    
    if args.plural:
        wn_browse('n', print_plural)
    elif args.singular:
        wn_browse('n', print_tag)
    else:
        wn_browse('n', print_combined)

def gen_verbs(args):
    wn_browse('v', print_tag)

def gen_adjs(args):
    wn_browse('a', print_tag)

def gen_advs(args):
    wn_browse('r', print_tag) 

def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help="fine level commands")

    parser_nouns = subparsers.add_parser('nouns', 
        help="generate nouns")
    group = parser_nouns.add_mutually_exclusive_group()
    group.add_argument('-p', '--plural', action="store_true", 
        help="generate plural instances of nouns")
    group.add_argument('-s', '--singular', action="store_true",
        help="generate singular instances of nouns")
    group.add_argument('-a', '--all', action="store_true",
        help="generate all instances of nouns, singular and plural")
    parser_nouns.set_defaults(func=gen_nouns)

    parser_verbs = subparsers.add_parser('verbs',
        help="generate verbs")
    parser_verbs.set_defaults(func=gen_verbs)
    
    parser_adjs = subparsers.add_parser('adjs',
        help="generate adjectives")
    parser_adjs.set_defaults(func=gen_adjs)

    parser_advs = subparsers.add_parser('advs',
        help="generate adverbs")
    parser_advs.set_defaults(func=gen_advs)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
