import nltk.data
import unicodedata
import sys
import json
import os


class SentenceSplitter:
	def __init__(self,in_dir,out_file):
		self.tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
		self.input_dir = in_dir
		self.out = open(out_file,"a")

	def tokenize(self,input_file):
		for line in input_file:
			js = json.loads(line)
			data = js["text"]
			url = js["url"]
			data_normal = unicodedata.normalize('NFKD', data).encode('ascii','ignore')
			arr = self.tokenizer.tokenize(data_normal)
			page = {"url":url,"text":arr}
			self.out.write(json.dumps(page))
			self.out.write("\n")

	def tokenize_all(self,direc):
		fileList = []
		rootdir = self.input_dir + direc + "/"
		for root, subFolders, files in os.walk(rootdir):
		    for file in files:
		        fileList.append(os.path.join(root,file))

		for file in fileList:
			in_file = open(file,"r")
			self.tokenize(in_file)


ss = SentenceSplitter("extracted_json/","wiki"+sys.argv[1])


ss.tokenize_all(sys.argv[1])
	
