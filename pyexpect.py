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
	
	tries_all["PERSON"] = marisa_trie.Trie().load("person.marisa")
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

#create ralations between multiple e1 and multiple e2
def breakRelations(all_relations):
	#print "all_relation", all_relations
	big_relation_store = []
	#print all_relations
	for rel in all_relations:
		#print "relation",rel
		for i in range(len(rel["e1"])):
			for j in range(len(rel["e2"])):
				big_relation_store.append({"e1":rel["e1"][i], "rel":rel["rel"], "e2":rel["e2"][j]})
	return big_relation_store

#map relations from annotations and patterns
def createRelations(annotations,pat,relations):
	#print annotations
	#print pat
	#print relations

	classMap = {}

	for i in range(len(pat)):
		if pat[i][1] in ["$","@"]:
			p = pat[i]
			if p.find("|") > -1:
				ps = p.split("|")
				for ps_i in ps:
					if ps_i[0] == "[":
						ps_i = ps_i[1:]
					elif ps_i[len(ps_i)-1] == "]":
						ps_i = ps_i[:len(ps_i)-1]
					classMap[ps_i] = i
			else:
				if p[len(p)-1] in ["+"]:
					p = p[1:len(p)-2]
				else:
					p = p[1:len(p)-1]
				classMap[p] = i

	print "classMap",classMap
	all_relations = []

	for rel in relations:
		one_relation = {}
		rels = rel.split("--")
		try:
			if rels[0][0] in ["$","@"]:
				i = classMap[rels[0]]
				#print i
				one_relation["e1"] = annotations[i]
			else:
				temp = []
				temp.append(rels[0])
				one_relation["e1"] = temp
		except:
			print rels[0],"is not found in classMap or annotations"


		one_relation["rel"] = rels[1]

		try:
			if rels[2][0] in ["$","@"]:
				i = classMap[rels[2]]
				one_relation["e2"] = annotations[i]
			else:
				temp = []
				temp.append(rels[2])
				one_relation["e2"] = temp
		except:
			print rels[2],"is not found in classMap or annotations"

		all_relations.append(one_relation)

	all_relations = breakRelations(all_relations)

	return all_relations

#init function
def extract_init(sent):
	
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
				extracts = createRelations(annotations,pat,relations)
				for ex in extracts:
					print ex
				#extractions = {}
				#extractions["extractions"] = extracts
				#json.dumps(extractions,indent = 4,separators=(',', ': '))

if __name__ == '__main__':	
	sent = "Charles Dickens wrote books like A Christmas Carol, Anthony and Mayan, A Chritmas Carol"
	sent1 = "hello from book A Christmas Carol, Anthony to kill me"

	persons = ["Bill Gates"]
	authors = ["Charles Dickens"]
	books = ["A Christmas Carol","Anthony","Mayan"]

	trie = {"PERSON":persons, "BOOK":books, "AUTHOR":authors}
	
	#test annotation
	ptrie = marisa_trie.Trie(pyannotate.toLowerCase(persons))
	btrie = marisa_trie.Trie(pyannotate.toLowerCase(books))
	#pyannotate.annotate(sent,ptrie,1)

	#test pattern indices
	start,end = getIndices(sent,"[C|c]arol")
	#print start, end

	#main
	initTries(trie)
	extract_init(sent)
	extract_init(sent1)
