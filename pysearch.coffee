cson = require "coffeeson"
fs = require "fs"

stream = fs.createReadStream("wiki2")

for_each_line = (strm,func) ->
	last = ""
	stream.on("data",(chunk) ->
		lines = (last + chunk).split("\n")
		[]
	)


matched = (pat_and,pat_or,pat_not,lin) ->
	pat_or_flag = false
	pat_and_flag = true
	pat_not_flag = true

	if pat_or.length == 0
		pat_or_flag = true
	else
		pat_or_flag = false
		for pat in pat_or
			m = lin.search(pat)
			if m > -1
				pat_or_flag = true
				break

	if pat_and.length == 0
		pat_and_flag = true
	else
		pat_and_flag = true
		for pat in pat_and
			m = lin.search(pat)
			if not (m > -1)
				pat_and_flag = false
				break
		
	if pat_not.length == 0
		pat_not_flag = true
	else
		pat_not_flag = true
		for pat in pat_not
			m = re.search(pat,lin)
			if m > -1
				pat_not_flag = false

	return (pat_not_flag and pat_and_flag and pat_or_flag)

cson.parseFile "search.json",(err,tree) -> 
	class_nodes = tree.classes
	console.log class_nodes
