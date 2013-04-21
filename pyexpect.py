import sys
import re
import json
import marisa_trie
import pyannotate

DEBUG = 0

#read the json file
def readJson():
	expect_file = open("expect.json","r")
	expect_json = json.load(expect_file)
	expect = expect_json["expectations"]
	return expect

#get start and end index of a regex pattern
def getIndices(sent,pattern):
	m = re.search(pattern,sent)
	if m:
		return m.start(),m.end()
	else:
		return -1,-1

def getLeftPatterns(patterns,i):
	return patterns[:i]

def getRightPatterns(patterns,i):
	return patterns[i+1:]

def partition(sent,patterns):
	if sent == "" or len(patterns) == 0:
		if len(patterns) == 0:
			return [sent]
		else:
			return [""]
	else:
		regexPattern = 0
		for i in range(len(patterns)):
			if not (patterns[i][1] in ["$","@"]):
				#print "pat",patterns[i]
				regexPattern = 1
				l = len(patterns[i].strip()) - 1 
				pat = patterns[i].strip()
				pat = pat[1:l]

				print pat

				start,end = getIndices(sent,pat)
				if start > -1:
					#print sent[start:end+1]
					left  = partition(sent[:start],getLeftPatterns(patterns,i))
					right = partition(sent[end+1:],getRightPatterns(patterns,i))
					return left + ["@"+pat] + right
				else:
					return [""]

		if regexPattern == 0:
			return [sent]

#init function
def extract_init(sent,classes):
	persons = pyannotate.toLowerCase(classes[0])
	books = pyannotate.toLowerCase(classes[0])

	ptrie = marisa_trie.Trie(persons)
	btrie = marisa_trie.Trie(books)

	exp = readJson()
	if DEBUG:
		print "json object = ",exp

	for exp_one in exp:

		if DEBUG:
			print "first element = ",exp_one

		patterns = exp_one["patterns"]

		if DEBUG == 0:
			print "patterns = ",patterns

		for pattern in patterns:
			pat = pattern.split(",")
			print partition(sent,pat)

if __name__ == '__main__':	
	sent = "Charles Dickens wrote books like A Christmas Carol, Anthony and Mayan, A Chritmas Carol"
	sent1 = "hello from book me to kill me"
	persons = [u"Charles Dickens"]
	books = [u"A Christmas Carol",u"Anthony",u"Mayan"]

	#test annotation
	ptrie = marisa_trie.Trie(pyannotate.toLowerCase(persons))
	btrie = marisa_trie.Trie(pyannotate.toLowerCase(books))
	#pyannotate.annotate(sent,ptrie)

	#test pattern indices
	start,end = getIndices(sent,"[C|c]arol")
	#print start, end

	#main
	extract_init(sent1,[persons,books])