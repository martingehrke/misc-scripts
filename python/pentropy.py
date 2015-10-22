#!/bin/env python
# calcaulate the entropy of a string
# include helpful info and time to crack
# wikipedia entry for future reference
#  https://en.wikipedia.org/wiki/Password_strength#Entropy_as_a_measure_of_password_strength

import argparse
import sys


def main(argv=None):

    if argv is None:
        argv = sys.argv	


    parser = argparse.ArgumentParser()


    parser.add_argument('-p','--password',help='password to examine',
                        action='store',dest='passwd',type=str)

    parser.add_argument('-g','--generate',help='generate and examine a new password',
                        action='store_true',dest='generate')

    args = parser.parse_args(argv[1:])


if __name__ == "__main__":
    sys.exit(not main());
