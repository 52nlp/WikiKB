import sys
import json

in_file = open(sys.argv[1],"r")
for line in in_file:
	jline = json.loads(line)
	url = jline["url"]
	text = jline["text"]
	if url.find(sys.argv[2]) > -1:
		print text[:3]
