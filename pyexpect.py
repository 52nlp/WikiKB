import sys
import re
import json
import marisa_trie
import pyannotate

DEBUG = 0
tries_all = {}

def trim(pat):
	pat_new = []
	for p in pat:
		pat_new.append(p.strip())
	return pat_new

def initTries(trie_dict):
	for k,v in trie_dict.iteritems():
		v_arr = []
		for value in v:
			v_arr.append(unicode(value,errors="ignore"))

		v_arr = pyannotate.toLowerCase(v_arr)
		tries_all[unicode(k,errors="ignore")] = marisa_trie.Trie(v_arr)
	#print tries_all

#get trie based on the pattern
def getTrie(key):
	return tries_all[key]

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

				#print pat

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

#annotate for OR operator
def annotateOR(part,pat,oneORmore):
	#print part
	annotations = []
	pats = pat.split("|")
	for p in pats:
		if p[0] in ["$","@"]:
			p = p[1:]
		#print p
		try:
			trie = getTrie(p)
			annotations += pyannotate.annotate(part,trie,oneORmore)
		except:
			print "No " + p + " class found" 

	return annotations


#annotate and find relations
def findRelations(parts,patterns):
	for i in range(len(patterns)):
		if patterns[i][1] in ["$","@"] and not parts[0] == "":
			oneORmore = 1

			l = len(patterns[i].strip()) - 2
			if patterns[i][l+1] == "]":
				oneORmore = 0
				l += 1

			pat = patterns[i].strip()
			pat = pat[2:l]

			#print pat,i, parts[i]
			if pat.find("|") > -1:
				annotations = annotateOR(parts[i].strip(),pat,oneORmore)
				print annotations
			else:
				try:
					trie = getTrie(pat)
					annotations = pyannotate.annotate(parts[i].strip(),trie,oneORmore)
					print annotations
				except:
					print "No " + pat + " class found"  


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

		for pattern in patterns:
			pat = pattern.split(",")
			pat = trim(pat)
			parts =  partition(sent,pat)

			#print parts

			findRelations(parts,pat)

if __name__ == '__main__':	
	sent = "Charles Dickens wrote books like A Christmas Carol, Anthony and Mayan, A Chritmas Carol"
	sent1 = "hello from book me to kill me"
	
	persons = ["Charles Dickens"]
	books = ["A Christmas Carol","Anthony","Mayan"]

	tries = {"PERSON":persons, "BOOK":books}

	#test annotation
	ptrie = marisa_trie.Trie(pyannotate.toLowerCase(persons))
	btrie = marisa_trie.Trie(pyannotate.toLowerCase(books))
	#pyannotate.annotate(sent,ptrie,1)

	#test pattern indices
	start,end = getIndices(sent,"[C|c]arol")
	#print start, end

	#main
	initTries(tries)
	extract_init(sent,[persons,books])