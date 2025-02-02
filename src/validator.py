#!/usr/bin/env python
# validator.py -q dataset.unique.val.txt

import re
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument("-q", "--queryfile", help="Path to input file")
args = parser.parse_args()
import sqlparser

queryfile="../sync_mtext_gen/dataset.unique.val.txt"

delimiter = re.compile('(<SOQ> | <EOQ>)')
valarg_regex = re.compile('(<VAL>|<ARG>)')
unk_regex = re.compile('<UNK>')
topunk_regex = re.compile('TOP <UNK>')
wild_regex = re.compile('<W>')

validset = open(args.queryfile+".valid", "w")
invalidset = open(args.queryfile+".invalid", "w")

with open(args.queryfile) as f:
    valid=0
    invalid=0
    parser = sqlparser.Parser()
    for line in f:
    	linein = line
    	line = re.sub(wild_regex, "*", line)
    	line = re.sub(topunk_regex, "TOP 10", line)
    	line = re.sub(delimiter, "", line)
    	lineVI = re.sub(valarg_regex, "10", line)
    	lineVX = re.sub(valarg_regex, "x", line)
    	lineUI = re.sub(unk_regex, "10", line)
    	lineUX = re.sub(unk_regex, "x", line)
    	lineUIVI = re.sub(unk_regex, "10", lineVI)
    	lineUIVX = re.sub(unk_regex, "10", lineVX)
    	lineUXVI = re.sub(unk_regex, "x", lineVI)
    	lineUXVX = re.sub(unk_regex, "x", lineVX)
    	if parser.check_syntax(line) == 0 || 
    		parser.check_syntax(lineVI) == 0 ||
    		parser.check_syntax(lineVX) == 0 ||
    		parser.check_syntax(lineUI) == 0 ||
    		parser.check_syntax(lineUX) == 0 ||
    		parser.check_syntax(lineUIVI) == 0 ||
    		parser.check_syntax(lineUIVX) == 0 ||
    		parser.check_syntax(lineUXVI) == 0 ||
    		parser.check_syntax(lineUXVX) == 0:
    		valid += 1
    		validset.write(linein)
    	else:
    		invalid += 1
    		invalidset.write(linein)

invalidset.close()
validset.close()

print "Valid:%d" % valid
print "Invalid:%d" % invalid
