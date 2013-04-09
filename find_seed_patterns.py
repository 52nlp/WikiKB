import re
import sys
import json



seeds = json.load(open("seed.json","r"))
#print seeds
patterns = {"patterns":[]}

for seed_rec in seeds["seeds"]:
	seed1_temp = str(seed_rec["seed1"])
	seed2_temp = str(seed_rec["seed2"])
	#print seed1,seed2
	relation = str(seed_rec["relation"])
	D1 = str(seed_rec["$1"])
	D2 = str(seed_rec["$2"])
	pattern = {"relation":relation,"pattern":[],"$1":D1,"$2":D2}

	input_file = open(sys.argv[1],"r")
	for line in input_file:
		#print line
		line = line.lower()
		seed1 = seed1_temp
		seed2 = seed2_temp
		seed1 = seed1.lower()
		seed2 = seed2.lower()
		seed1_index = line.find(seed1)
		seed2_index = line.find(seed2)

		#print seed1_index,seed2_index

		if seed1_index > -1 and seed2_index > -1:
			if seed1_index < seed2_index:
				pat_start_index = seed1_index + len(seed1)
				pat_end_index = seed2_index 
				one = seed1
				two = seed2

			elif seed1_index > seed2_index:
				pat_start_index = seed2_index + len(seed2)
				pat_end_index = seed1_index
				one = seed2
				two = seed1

			words = line[pat_start_index:pat_end_index].strip().split(" ")
			if len(words) < 10:
				pattern["pattern"].append(line[pat_start_index:pat_end_index])
	if not len(pattern["pattern"]) == 0:
		patterns["patterns"].append(pattern)		
	input_file.close()

new_file = open("new_pattern.json","w")
new_file.write(json.dumps(patterns,indent = 4,separators=(',', ': ')))
print json.dumps(patterns,indent = 4,separators=(',', ': '))
