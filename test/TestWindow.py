# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE
from __future__ import division
import os
from locale import gettext as _

from gi.repository import Gtk # pylint: disable=E0611
from gi.repository.GdkPixbuf import Pixbuf, InterpType
# from gi.repository.GdkImage import Image
import logging
logger = logging.getLogger('test')
from PIL import Image
from test_lib import Window
from test.AboutTestDialog import AboutTestDialog
from test.ManualModeDialog import ManualModeDialog
from test.PreferencesTestDialog import PreferencesTestDialog
import sys
sys.path.append("/home/ishaan/Desktop/cs315/project/pdf-fondler/test/db_script")
from lda_api import lda_api
from mongodb_script import search_in_db
from multiprocessing import Pool
# See test_lib.Window.py for more details about how this class works
class TestWindow(Window):
    __gtype_name__ = "TestWindow"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(TestWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutTestDialog
        self.ManualMode = ManualModeDialog
        self.PreferencesDialog = PreferencesTestDialog
        self.keywordField = self.builder.get_object("keywordField")
        self.treeview = self.builder.get_object("treeView")
        self.imageGrid = self.builder.get_object("imageGrid")
        self.model = self.builder.get_object("model") #this is lisStore
        # self.model_new = self.builder.get_object("model_new")
        self.selectedFiles = []
        # Code for other initialization actions should be added here.
    
    def on_keywordField_activate(self, widget):
        searchString =  widget.get_text()      
        img_list = search_in_db(searchString)
        self.model.clear()
        for col in self.treeview.get_columns():
            self.treeview.remove_column(col)
         
        # print img_list.count()
        for img in img_list:
                
            im=Image.open(img['img_file_path'])
            # im.size
            # img_pixbuf = Pixbuf.new_from_file(img['img_file_path']).scale_simple(800,800,InterpType.BILINEAR)
            # image = Gtk.Image.new_from_pixbuf(img_pixbuf)
            # if(i%2==0):
            # self.imageGrid.attach(image,i%2,i,1,1)
            # else:
                # self.imageGrid.attach(image,0,i,1,1)
            # i=i+1    

            # self.model.append([(Pixbuf.new_from_file(img['img_file_path'])),img['file_path']])#treeitr the index in liststore to which entry is done
            self.model.append([(Pixbuf.new_from_file(img['img_file_path'])).scale_simple(900,(im.size[1]/im.size[0])*900,InterpType.BILINEAR),img['file_path']])#treeitr the index in liststore to which entry is done
            # self.model.append([Pixbuf.new_from_file(img['img_file_path'],img['colorspace'],img['has_alpha'],img['bits_per_sample'],img['width'],img['height'],img['rowstride']),img['img_file_path']])#treeitr the index in liststore to which entry is done

        # print searchString
        # print "MODEL\n"
        # print self.model

        #HERE we connect with database and retrieve from it the various entries
        # and then we populate the list and display images. 
        #after recieving things from Arnab's wrapper
       # model = Gtk.ListStore(Gtk.gdk.Pixbuf, str) #str will contain image-file-names
        #treeview = Gtk.TreeView(model) #need modifications when rendering
        # self.model.append([Pixbuf.new_from_data('data/media/background.png'),'data/media/background.png'])#treeitr the index in liststore to which entry is done
        # self.model.append([Pixbuf.new_from_file('data/media/download.jpg'),'data/media/download.jpg'])
       # self.model.append([Pixbuf.new_from_file('data/media/background.png'),Pixbuf.new_from_file('data/media/download.jpg')])

        # renderer.set_fixed_size(100)

        self.treeview.set_model(self.model)
        renderer = Gtk.CellRendererPixbuf()
        renderer.set_padding(10,20)
        # rendere.set_
        column = Gtk.TreeViewColumn('',renderer, pixbuf=0)
        column.set_spacing(-1)
        # column.set_attribute()
        self.treeview.insert_column(column,0)
        # print column.get_spacing()
        


        # column.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
        # column.set_fixed_width(500)
        # column.set_max_height(200)
        # self.treeview.remove_column(column)
        # self.treeview.insert_column(column,1)
        #column = Gtk.TreeViewColumn('Icon',renderer, pixbuf=1)
        #column = Gtk.TreeViewColumn()
        #self.treeview.append_column(column)

        #title = Gtk.CellRendererPixbuf()
        #author = Gtk.CellRendererPixbuf()

        #column.pack_start(title, True)
        #column.pack_start(author, True)

        #column.add_attribute(title, "pixbuf", 0)
        #column.add_attribute(author, "pixbuf", 1)

        #self.treeview.append_column(column)
       # renderer = Gtk.CellRendererText()
        #column = Gtk.TreeViewColumn('Text', renderer, text=1)
        #self.treeview.append_column(column)
        
    def on_addToBasket_clicked(self,widget):
        selection = self.treeview.get_selection()
        (model, pathlist) = selection.get_selected_rows()
        for path in pathlist :
            tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter,1)
            self.selectedFiles.append(value)
            print value   
    def on_startOver_clicked(self,widget):
    #clear the screen and selectedFiles buffer
        self.model.clear()       
        print "here"  
    
    def on_openSelected_clicked(self,widget):
        for filePath in self.selectedFiles:
            k = filePath.rfind("_")
            nfilePath=filePath[0:k]
            os.system("gnome-open "+ nfilePath+".pdf")
        print "here1"     
        # HERE we will open various files

    def on_doneSelection_clicked(self,widget):
        self.model.clear()
        files=""
        for filePath in self.selectedFiles:
            print filePath #write appropriate code to load these files
            files=files+" "+filePath 
        os.system("pdftk" + files +" cat output mergedfile.pdf")    
    def on_addToIndex_clicked(self,widget):
        dialog = Gtk.FileChooserDialog("Please choose a file", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        filter_text = Gtk.FileFilter()
        filter_text.set_name(".pdf")
        filter_text.add_mime_type("application/pdf")
        dialog.add_filter(filter_text)
        file_name=""
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + dialog.get_filename())
            file_name = dialog.get_filename()
            #INSERT CODE HERE TO INDEX FILE
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

        pool = Pool(processes=1)              # Start a worker processes.
        result = pool.apply_async(lda_api, [file_name])
        # p = Process(target=, args=)
        # p.start()
        # dialog = Gtk.FileChooserDialog("Open..",None,Gtk.FILE_CHOOSER_ACTION_OPEN,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
        # dialog.set_default_response(Gtk.RESPONSE_OK)
        # response = dialog.run()

      #  if Gtk_dialog_run(Gtk_DIALOG (dialog)) == Gtk_RESPONSE_ACCEPT:
       #     print "yes"
#       else:
 #           print "no"
#        Gtk_widget_destroy (dialog);
        


