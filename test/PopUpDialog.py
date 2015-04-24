# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

from locale import gettext as _

import logging
logger = logging.getLogger('test')

# from test_lib.AboutDialog import AboutDialog
from gi.repository import Gtk
from test_lib.helpers import get_builder
from test_lib.callback import cell_edited_callback
import sys
sys.path.append("/home/ishaan/Desktop/cs315/project/pdf-fondler/test/db_script")
from mongodb_script import get_all


# See test_lib.AboutDialog.py for more details about how this class works.
class PopUpDialog(Gtk.Dialog):
    __gtype_name__ = "PopUpDialog"
    
    def __new__(cls):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated AboutDialog object.
        """
        builder = get_builder('PopUpDialog')
        new_object = builder.get_object("popup_dialog")

        
        treeview = builder.get_object("popupView")
        model = builder.get_object("popupStore") #this is lisStore

        all_files = get_all()
        for file_name, page_tag_dict in all_files.iteritems(): 
            parent = model.append(None,[file_name,'',False])
            for page_num, tags in page_tag_dict.iteritems():
                model.append(parent,["Page "+page_num,tags,True])

        treeview.set_model(model)
        renderer = Gtk.CellRendererText()
        renderer.set_padding(10,20)
        # rendere.set_
        column = Gtk.TreeViewColumn('File Name',renderer, text=0)

        renderer1 = Gtk.CellRendererText()
        renderer1.set_padding(10,20)
        # rendere.set_
        column1 = Gtk.TreeViewColumn('Tags',renderer1, text=1,editable=2)
        renderer1.connect('edited', cell_edited_callback,model)
        # column.set_spacing(-1)
        # column.set_attribute()
        treeview.insert_column(column,0)
        treeview.insert_column(column1,1)


        # new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
    #     """Called while initializing this instance in __new__

    #     finish_initalizing should be called after parsing the ui definition
    #     and creating a AboutDialog object with it in order
    #     to finish initializing the start of the new AboutTestDialog
    #     instance.
        
    #     Put your initialization code in here and leave __init__ undefined.
    #     """
        self.builder = builder
        self.ui = builder.get_ui(self)
    # def        
