
from locale import gettext as _

import logging
logger = logging.getLogger('test')

# from test_lib.AboutDialog import AboutDialog
from gi.repository import Gtk
import sys
sys.path.append("/home/ishaan/Desktop/cs315/project/pdf-fondler/test/db_script")
from mongodb_script import update_db_tag

def cell_edited_callback(renderer,path,text,model):
	print renderer
	print path
	print text
	print model
	child = model.get_iter(Gtk.TreePath.new_from_string(path))
	model.set_value(child,1,text)
	parent_iter = model.iter_parent(child)
	file_name = model.get_value(parent_iter,0) +"_"+ model.get_value(child,0).split()[1]+".pdf"
	update_db_tag(file_name,text)
	


	# treerowref.tag = text

	# model.set_row(treerowref,)