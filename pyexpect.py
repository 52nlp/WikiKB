import sys
import re
import json
import marisa_trie

DEBUG = 1

#read the json file
def readJson():
	expect_file = open("expect.json","r")
	expect_json = json.load(expect_file)
	expect = expect_json["expectations"]
	return expect

#main function
def main():
	exp = readJson()
	if DEBUG:
		print "json object = ",exp

	for exp_one in exp:
		if DEBUG:
			print "first element = ",exp_one
		patterns = exp_one["patterns"]
		if DEBUG:
			print "patterns = ",patterns


if __name__ == '__main__':	
	main()