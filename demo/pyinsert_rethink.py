import rethinkdb as r


def connect_r(port):
	return r.connect("localhost",port)

def insert_r(conn,table,sent,rel,val):
	bulk = {}
	if isinstance(rel["e1"],unicode):
		bulk["e1"] = rel["e1"]
	else:
		bulk["e1"] = unicode(rel["e1"],errors="ignore")

	if isinstance(rel["rel"],unicode):
		bulk["rel"] = rel["rel"]
	else:
		bulk["rel"] = unicode(rel["rel"],errors="ignore")

	if isinstance(rel["e2"],unicode):
		bulk["e2"] = rel["e2"]
	else:
		bulk["e2"] = unicode(rel["e2"],errors="ignore")

	if isinstance(sent,unicode):
		bulk["sent"] = sent
	else:
		bulk["sent"] = unicode(sent,errors="ignore")

	bulk["cfval"] = val
		

	r.db("wikikb").table(table).insert(bulk).run(conn)

def delete_table_r(conn,table):
	r.db("wikikb").table(table).delete().run(conn)

if __name__ == '__main__':
	conn = connect_r(36903)
	insert_r(conn,"demo1","hello this is a test sentence",{"e1":"test e1","rel":"test rel","e2":"test e2"},1)