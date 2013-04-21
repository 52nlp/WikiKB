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

		#no regex pattern found only class pattern are found
		if regexPattern == 0:
			mul = len(patterns)
			return [sent]*mul

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


#annotate parts
def createAnnotations(parts,patterns):
	types = {}

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
				#print annotations
				types[i] = annotations
			else:
				if pat[len(pat)-2] == "_":
					pat = pat[:len(pat)-2]
				try:
					trie = getTrie(pat)
					annotations = pyannotate.annotate(parts[i].strip(),trie,oneORmore)
					#print annotations
					types[i] = annotations
				except:
					print "No " + pat + " class found"  

	return types

#add dummy regex pattern or add dummy class to make the pat same size as parts
def augumentPat(pat):
	if not pat[0][1] in ["$","@"]:
		pat = ["[$DUMMY]"] + pat
	if not pat[0][1] in ["$","@"]:
		pat =  pat + ["[$DUMMY]"]
	
	prev = pat[0]	
	i = 0
	while i < (len(pat) - 1):
		if (not (pat[i][1] in ["$","@"])) and (not (prev[1] in ["$","@"])):
			pat = pat[:i] + ["[$DUMMY]"] + pat[i:]
		prev = pat[i]
		i += 1
	return pat

#map relations from annotations and patterns
def createRelations(annotations,pat,relations):
	print annotations
	print pat
	print relations

	classMap = {}

	for i in range(len(pat)):
		


	return annotations

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
		relations = exp_one["relations"]

		if DEBUG:
			print "patterns = ",patterns

		for pattern in patterns:
			pat = pattern.split(",")
			pat = trim(pat)
			pat = augumentPat(pat)

			parts =  partition(sent,pat)

			#print parts,len(parts)
			#print pat,len(pat)

			if len(parts) == len(pat):
				annotations = createAnnotations(parts,pat)
				print createRelations(annotations,pat,relations)

if __name__ == '__main__':	
	sent = "Charles Dickens wrote books like A Christmas Carol, Anthony and Mayan, A Chritmas Carol"
	sent1 = "hello from book A Christmas Carol, Anthony to kill me"
	
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