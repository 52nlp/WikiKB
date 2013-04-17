import rethinkdb as r



f = open("../yagoFacts.ttl")

def tocsv(ifile):
	print ",".join(["e1","rel","e2"])
	for line in ifile:
		
		if line[0] == '#' or len(line) < 10 or line[0] == '@':
			continue
		line = line[:len(line)-2].replace("<","").replace(">","").strip()
		line_arr = line.split("\t")
	
		e1 = unicode(line_arr[0],errors="ignore").replace(",","|")
		r = unicode(line_arr[1],errors="ignore")
		e2 = unicode(line_arr[2],errors="ignore").replace(",","|")
		print ",".join([e1,r,e2])
	print ",".join(["e1","rel","e2"])

tocsv(f)