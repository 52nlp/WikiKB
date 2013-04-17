import re
import sys
import json


class_file = open("classes.json","r")

#pat = sys.argv[1]
#start = 0

def matched(pat_and,pat_or,pat_not,lin):
	pat_or_flag = False
	pat_and_flag = True
	pat_not_flag = True

	if len(pat_or) == 0:
		pat_or_flag = True
	else:
		pat_or_flag = False
		for pat in pat_or:
			m = re.search(pat,lin)
			if m:
				#print lin
				pat_or_flag = True
				break

	if len(pat_and) == 0:
		pat_and_flag = True
	else:
		pat_and_flag = True
		for pat in pat_and:
			m = re.search(pat,lin)
			if not m:
				pat_and_flag = False
				break

		
	if len(pat_not) == 0:
		pat_not_flag = True
	else:
		pat_not_flag = True
		for pat in pat_not:
			m = re.search(pat,lin)
			if m:
				pat_not_flag = False

	return (pat_not_flag and pat_and_flag and pat_or_flag)

cls = json.load(class_file)

class_nodes = cls["classes"]

all_classes_match = {}
for class_patterns in class_nodes:
	all_classes_match[class_patterns["name"]] = {"matches":[],"total":0}

#print len(class_nodes)
ifile = open(sys.argv[1],"r")
for line in ifile:
	for class_patterns in class_nodes:
		pat_and = class_patterns['pattern-and']
		pat_or = class_patterns['pattern-or']
		pat_not = class_patterns['pattern-not']

		#print pat_and,pat_or,pat_not
	
		start = int(class_patterns["start"])
		end = int(class_patterns["end"])

		data = json.loads(line)
		url = data["url"]
		txt = data["text"]

		#print len(txt)
		flag = False
		output = {"url":url,"match":[]}

		if end == -1:
			end = len(txt)

		#print start,end

		for lin in txt[start:end]:
			flag_match = False
			flag_match = matched(pat_and,pat_or,pat_not,lin)

			if flag_match:
				output["match"].append(lin)
				flag = True

		if flag:
			flag = False
			all_classes_match[class_patterns["name"]]["matches"].append(output)
			all_classes_match[class_patterns["name"]]["total"] += len(output["match"])

print json.dumps(all_classes_match,indent = 4,separators=(',', ': '))