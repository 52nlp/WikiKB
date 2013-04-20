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


def extract(sent,patterns):
	if sent == "":
		return 
	else:
		for pat in patterns:
			start,end = getIndices(sent,pat)
			if start > -1:
				extract(sent[:start],)

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
		if DEBUG:
			print "patterns = ",patterns


if __name__ == '__main__':	
	sent = "Charles Dickens wrote books like A Christmas Carol, Anthony and Mayan, A Chritmas Carol"
	persons = [u"Charles Dickens"]
	books = [u"A Christmas Carol",u"Anthony",u"Mayan"]

	#test annotation
	ptrie = marisa_trie.Trie(pyannotate.toLowerCase(persons))
	btrie = marisa_trie.Trie(pyannotate.toLowerCase(books))
	#pyannotate.annotate(sent,ptrie)

	#test pattern indices
	start,end = getIndices(sent,"[C|c]arol")
	print start, end

	#main
	extract_init(sent,[persons,books])