import sys
import json
import urllib as ul
import marisa_trie

files = {"LOCATION":["location1.json","location2.json"],"PERSON":["person1.json","person2.json"],"AUTHOR":["author1.json","author2.json"]}
ofile = open(sys.argv[1],"w")
lst = []

for file_name in files[sys.argv[1]]:
	print file_name
	name = "./class/" + file_name
	f = open(name,"r")

	jf = json.load(f)

	classes = jf[sys.argv[1]]
	matches = classes["matches"]

	for m in matches:
		url_arr = m["url"].split("/")
		title = url_arr[len(url_arr)-1]
		title = title.split("_")
		title = " ".join(title)
		title = title.lower()
		lst.append(title)
		ofile.write(title)
		ofile.write("\n")

trie = marisa_trie.Trie(lst)
"""
if u"bill gates" in trie:
	print "YES"
"""
trie.save(sys.argv[1]+".marisa")