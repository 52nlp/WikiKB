import sys
import re
import json
import dawg

persons = [u'Charles Dickens',u'Bill Gates']
person_dawg = dawg.DAWG(persons)
books = [u'A christmas carol',u'Alchemist']
book_dawg = dawg.DAWG(books)

trie = {"$BOOK":book_dawg,"$PERSON":person_dawg}

sent = "English writer Charles Dickens wrote A Christmas Carol, The Chimes, The Cricket on the Hearth and several other books."

j_file = open("expect.json","r")
e_json = json.load(j_file)

expectaions = e_json['expectations']

def search(patterns,start,end,line):
	for i in range(start,end):
		pass

def main():
	for expect in expectaions:
		for pat in expect["patterns"]:
			pats = pat.split(" ")
			for p in pats:
				if not p[1] == "$":
					if re.search(p[1:len(p)],sent):
						index = pats.index(p)
						left = search(pats,0,index,sent)
						right = search(pats,index,len(pats),sent)
					else:
						break
				else:
					pass