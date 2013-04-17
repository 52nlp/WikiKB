import rethinkdb as r

conn = r.connect("localhost",37105)

f = open("../yagoFacts.ttl")

def bulk_insert(ifile):
	bulk_size = 1000
	i = 0
	bulk_ins = []
	bulk = {}
	for line in ifile:
		bulk = {}
		if line[0] == '#' or len(line) < 10 or line[0] == '@':
			continue
		line = line[:len(line)-2].replace("<","").replace(">","").strip()
		line_arr = line.split("\t")
		print line_arr,i
		bulk["id"] = unicode(line_arr[0],errors="ignore")
		bulk["rel"] = unicode(line_arr[1],errors="ignore")
		bulk["id2"] = unicode(line_arr[2],errors="ignore")

		if i < bulk_size - 1:
			bulk_ins.append(bulk)
			i += 1
		elif i == bulk_size - 1:
			bulk_ins.append(bulk)
			r.db("yago").table("test").insert(bulk_ins).run(conn)
			i = 0


	if i < bulk_size - 1 and i > 0:
		bulk_ins.append(bulk)
		r.db("yago").table("test").insert(bulk_ins).run(conn)


bulk_insert(f)