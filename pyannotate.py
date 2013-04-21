import sys
import re
import json
import marisa_trie

#persons = [u'Charles Dickens',u'Bill Gates']
#test_trie = marisa_trie.Trie(persons)


def toLowerCase(arr):
	temp = []
	for a in arr:
		temp.append(a.lower())
	return temp


def removeRubbish(grams):
	rubbish = [",",".",";"]
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

def sortByLength(arr):
	for i in range(len(arr)-1):
		for j in range(i+1,len(arr)):
			if len(arr[i]) < len(arr[j]):
				arr[i],arr[j] = arr[j],arr[i]
	return arr

def annotate(sent,trie,oneORmore):
	onegrams = sent.split(" ")
	onegrams = removeRubbish(onegrams)
	sent = " ".join(onegrams)

	annotations = []
	#print sent
	#print onegrams
	i = 0
	foundAtLeatOne = 0
	while i < len(onegrams) - 1:
		#print "iteration = ",i
		found = 0
		st = onegrams[i].lower().strip() + " " +onegrams[i+1].lower().strip()
		st = unicode(st,errors="ignore")
		#print "key",st
		if st in trie:
			#print "#################found_whole = ",st
			annotations.append(st)
			found = 1
			foundAtLeatOne = 1
			i += 1
		else:
			#print "String searching for = ",st
			tk = trie.keys(st)

			if len(tk) > 0:
				#print tk
				length = i-len(onegrams[i])
				#print onegrams[i]
				#print i
				for k in range(i+1):
					length += len(onegrams[k])

				tk = sortByLength(tk)
				

				for tk_i in tk:
					#print "key = ",tk_i
					prev = ""
					n_st = sent[length:length+len(tk_i)]
					n_st = unicode(n_st,errors="ignore")
					#print "FINDING = ",n_st
					n_st = n_st
					if n_st in trie and len(n_st) > len(prev):
						#print "#################found = ",n_st
						annotations.append(n_st)
						prev = n_st[:]
						found = 1
						foundAtLeatOne = 1
						i = i+ len(n_st.split(" "))
						#print i
						break
		
		#print found, i
		if found == 0:
			arr2 = st.strip().split(" ")
			if arr2[0] in trie:
				found == 1
				foundAtLeatOne = 1
				#print "#################found_single_0 = ",arr2[0]
				annotations.append(arr2[0])

			if i == len(onegrams) - 2:
				found == 1
				foundAtLeatOne = 1
				if st.split(" ")[1] in trie:
					#print "#################found_single_1 = ",st.split(" ")[1]
					annotations.append(st.split(" ")[1])
			i += 1
		
		if found == 1 and not oneORmore:
			#print "one only"
			return annotations

	if i == len(onegrams) -1 and (oneORmore or ((not oneORmore) and foundAtLeatOne == 0)):
		if unicode(onegrams[i].strip(),errors="ignore") in trie:
			annotations.append(onegrams[i].strip())
	return annotations
					

def main():
	books = [u"A Christmas Carol",u"A Christmas Caroll",u"The Cricket on the Hearth",u"English writer Charles Dickens",u"Gates",u"Carol",u"hearth"]
	#books = [u"A Christmas Carol",u"The Cricket on the Hearth",u"English writer Charles Dickens"]

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

	sent = "Bill Gates shahrukh khan English writer Charles Dickens wrote A Christmas Caroll, The Chimes, The Cricket on the Hearth and several other books Gates."

	print annotate(sent,ptrie,1)


if __name__ == '__main__':
	#main()

	s = "A Christmas Carol, Anthony"
	books = ["A Christmas Carol","Anthony","Mayan"]
	books = toLowerCase(books)
	btrie = marisa_trie.Trie(books)
	print annotate(s,btrie,1)