import sys
import re
import json
import marisa_trie

#persons = [u'Charles Dickens',u'Bill Gates']
#test_trie = marisa_trie.Trie(persons)
rubbish = [",",".",";"]

def toLowerCase(arr):
	temp = []
	for a in arr:
		temp.append(a.lower())
	return temp


def removeRubbish(grams):
	ngrams = []
	for one in grams:
		one = one.strip()
		#print one
		if one[0] in rubbish:
			one = one[1:]
		if one[len(one)-1] in rubbish:
			#print "have rubbish in end"
			one = one[:len(one)-1]
			#print "After rubbish removed = ",one
		ngrams.append(one.lower())

	return ngrams

def annotate(sent,trie):
	onegrams = sent.split(" ")
	onegrams = removeRubbish(onegrams)
	sent = " ".join(onegrams)
	#print sent
	#print onegrams

	for i in range(len(onegrams)-1):
		st = onegrams[i].lower().strip() + " " +onegrams[i+1].lower().strip()
		st = unicode(st,errors="ignore")
		#print "key",st
		if st in trie:
			print "found = ",st
		else:
			tk = trie.keys(st)

			if len(tk):
				#print tk
				length = i-len(onegrams[i])
				#print onegrams[i]
				#print i
				for k in range(i+1):
					length += len(onegrams[k])
				for tk_i in tk:
					#print tk_i
					n_st = sent[length:length+len(tk_i)]
					n_st = unicode(n_st,errors="ignore")
				#print n_st
				
				if n_st in trie:
					print n_st
					i = i+ len(n_st.split(" "))
		#if one word in in the trie?

def main():
	books = [u"A Christmas Carol",u"The Cricket on the Hearth",u"English writer Charles Dickens"]
	#books = [u"A Christmas Carol",u"A Christmas Carol",u"The Cricket on the Hearth",u"English writer Charles Dickens"]

	books = toLowerCase(books)

	btrie = marisa_trie.Trie(books)

	
	"""
	per = open("person.list","r")

	persons = [] 
	for l in per:
		persons.append(unicode(l.strip().lower(),errors="ignore"))

	trie = marisa_trie.Trie(persons)

	trie.save("person.marisa")
	"""

	ptrie = marisa_trie.Trie()
	ptrie.load("person.marisa")

	sent = "English writer Charles Dickens wrote A Christmas Carol, The Chimes, The Cricket on the Hearth and several other books."

	annotate(sent,btrie)


main()