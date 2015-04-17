import pymongo
import os
from pymongo import MongoClient
from gi.repository import Gtk # pylint: disable=E0611
from gi.repository.GdkPixbuf import Pixbuf, InterpType
import sys
import time
# from lda_api.py import lda_api1
# import "../interactive-pdf-master/lda_api.py"
def insert_in_db(dict_object):#this function gets the dict object discussed. The object contains multiple pages of the same file usually
	client = MongoClient()
	
	db = client['pdf_interactive']
	pdf_collection = db['pdf_collection']
	to_insert=[]
	img_insert=[]
	print dict_object
	for file_path, tag_dict_array in dict_object.iteritems():
		for key_value_pair in tag_dict_array:
				tag_name = key_value_pair['tag']
				tag_weight = key_value_pair['weight']
				temp_doc={"tag":tag_name,"weight":tag_weight,"file_path":file_path,"img_file_path":file_path.split('.')[0]+".jpg"}
				to_insert.append(temp_doc)

		img_file_path = (file_path.split('.'))[0]+".jpg"
		# print file_path
		# print img_file_path
		os.system("convert -density 300 -trim "+ file_path +" -quality 100 "+img_file_path )
		# time.sleep(100)
		# img_temp_buf=Pixbuf.new_from_file(img_file_path)
		# img_data=img_temp_buf.get_pixels_array()
		# print img_data
		# exit(0)
		# img_data=img_temp_buf.get_pixels_array().encode('utf-8')
		 # def gtk.gdk.pixbuf_new_from_data(data, colorspace, has_alpha, bits_per_sample, width, height, rowstride)
		temp_img_doc={"img_file_path":img_file_path}# "data":img_temp_buf, "colorspace": img_temp_buf.get_colorspace(),"has_alpha":img_temp_buf.get_has_alpha(),"bits_per_sample":img_temp_buf.get_bits_per_sample(),"width":img_temp_buf.get_width(),"height":img_temp_buf.get_height(),"rowstride":img_temp_buf.get_rowstride()}
		img_insert.append(temp_img_doc)
		# os.system("rm "+img_file_path)
		
	result = pdf_collection.insert_many(to_insert)
	result.inserted_ids

	img_collection = db['img_collection']
	result = img_collection.insert_many(img_insert)
	result.inserted_ids

		#code to create the database
def search_in_db(search_string):
	client = MongoClient()
	# search_string=search_string.lower()
	db = client['pdf_interactive']
	pdf_collection = db['pdf_collection']
	img_collection = db['img_collection']
	
	result_img_list=[]
	print pdf_collection.find({"tag": search_string}).sort("weight")
	# exit(0)
	return pdf_collection.find({"tag": search_string}).sort("weight")
		# result_img_list.append(result))

	# return result_img_list

# search("hello")

	
