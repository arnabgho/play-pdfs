import os
import codecs
from gensim import corpora, models, similarities
from gensim.models import hdpmodel, ldamodel
from itertools import izip
from nltk.corpus import stopwords
import subprocess
from mongodb_script import insert_in_db
import string

def lda_api(filename_path):
	print filename_path
	# numPages=os.system("pdftk a.pdf dump_data | grep NumberOfPages | awk '{print $2}'")
	nfilename_path=filename_path.split('.')[0]
	print nfilename_path
	batcmd="pdftk " + filename_path + " dump_data | grep NumberOfPages | awk '{print $2}'"
	numPages = subprocess.check_output(batcmd, shell=True)
	os.system("pdftk "+ filename_path  +" burst output " + nfilename_path + "_%d.pdf compress")
	n=int(numPages)
	ret=[]
	tag_dict={}
	for i in range(1,n+1):
		nP=str(i)
		os.system("pdftotext -layout " +nfilename_path+"_"+nP+".pdf output.txt")

		with open("output.txt") as myfile:
		    raw="".join(line.rstrip() for line in myfile)


		raw= raw.decode('utf-8')
		document=''' '''
		for s in raw:
			document=document+s
		# documents=raw

		documents=[document]

		# print documents

		stoplist = set(stopwords.words("english"))
		# stoplist = set('by is his as was with at it for a of the and to in'.split())
		texts = [[word for word in document.lower().split() if word not in stoplist]
		         for document in documents]



		# remove words that appear only once
		all_tokens = sum(texts, [])
		tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
		texts = [[word for word in text if word not in tokens_once]
		         for text in texts]

		# print texts

		dictionary = corpora.Dictionary(texts)
		corpus = [dictionary.doc2bow(text) for text in texts]

		# I can print out the topics for LSA
		lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)
		corpus_lsi = lsi[corpus]

		# for l,t in izip(corpus_lsi,corpus):
		#   print l,"#",t
		# print

		res=""
		for topic in lsi.show_topics(1,5):
		  res= res+ topic
	
		res_list=res.split(' + ')
		tag_list=[]
		for r in res_list:
			l = len(r)
			pos=0
			for i in range(0,l):
				if r[i]=='*':
					pos=i
					break
			weight=r[0:pos]
			tag=r[pos+2:l-1]
			exclude=set(string.punctuation)-set('"')
			tag = ''.join(ch for ch in tag if ch not in exclude)
			w="weight"
			t="tag"	
			# dict={ "weight":weight,"tag":tag}
			dict={}
			dict[t]=tag
			dict[w]=weight
			# print "weight: "+dict[w]
			# print "tag: "+dict[t]
			tag_list.append(dict)

		# print tag_list
		tag_dict[nfilename_path+"_"+nP+".pdf"]=tag_list	
		ret.append(tag_dict)
		# print res_list
		print "-----------------------------------"
		# os.system(" rm " +filename_path+"_"+nP+".pdf")		
	# return tag_dict
	insert_in_db(tag_dict)	
# lda_api("/home/arnab/Interactive-pdf/a.pdf")	