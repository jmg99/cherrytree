# -*- coding: UTF-8 -*-
#
#       support.py
#       
#       Copyright 2009-2011 Giuseppe Penone <giuspen@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import gtk, os
import cons


def windows_cmd_prepare_path(filepath):
   """Prepares a Path to be digested by windows command line"""
   if not cons.CHAR_DQUOTE in filepath: return cons.CHAR_DQUOTE + filepath + cons.CHAR_DQUOTE
   elif not cons.CHAR_SQUOTE in filepath: return cons.CHAR_SQUOTE + filepath + cons.CHAR_SQUOTE
   return None

def dialog_file_save_as(filename=None, filter_pattern=None, filter_name=None, curr_folder=None, parent=None):
   """The Save file as dialog, Returns the retrieved filepath or None"""
   chooser = gtk.FileChooserDialog(title=_("Save File as"),
                                   action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                   buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK) )
   if parent != None: chooser.set_transient_for(parent)
   if curr_folder == None or os.path.isdir(curr_folder) == False:
      chooser.set_current_folder(os.path.expanduser('~'))
   else:
      chooser.set_current_folder(curr_folder)
   if filename != None:
      chooser.set_current_name(filename)
   if filter_pattern != None:
      filter = gtk.FileFilter()
      filter.set_name(filter_name)
      filter.add_pattern(filter_pattern)
      chooser.add_filter(filter)
   if chooser.run() == gtk.RESPONSE_OK:
      filepath = chooser.get_filename()
      chooser.destroy()
      return filepath
   else:
      chooser.destroy()
      return None

def dialog_file_select(filter_pattern=None, filter_name=None, curr_folder=None, parent=None):
   """The Select file dialog, Returns the retrieved filepath or None"""
   chooser = gtk.FileChooserDialog(title = _("Select File"),
                                   action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                   buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK) )
   if parent != None: chooser.set_transient_for(parent)
   if curr_folder == None or os.path.isdir(curr_folder) == False:
      chooser.set_current_folder(os.path.expanduser('~'))
   else:
      chooser.set_current_folder(curr_folder)
   if filter_pattern != None:
      filter = gtk.FileFilter()
      filter.set_name(filter_name)
      filter.add_pattern(filter_pattern)
      chooser.add_filter(filter)
   if chooser.run() == gtk.RESPONSE_OK:
      filepath = chooser.get_filename()
      chooser.destroy()
      return filepath
   else:
      chooser.destroy()
      return None
   
def dialog_folder_select(curr_folder=None, parent=None):
   """The Select folder dialog, returns the retrieved folderpath or None"""
   chooser = gtk.FileChooserDialog(title = _("Select Folder"),
                                   action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                                   buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK) )
   if parent != None: chooser.set_transient_for(parent)
   if curr_folder == None or os.path.isdir(curr_folder) == False:
      chooser.set_current_folder(os.path.expanduser('~'))
   else:
      chooser.set_current_folder(curr_folder)
   if chooser.run() == gtk.RESPONSE_OK:
      folderpath = chooser.get_filename()
      chooser.destroy()
      return folderpath
   else:
      chooser.destroy()
      return None
   
def dialog_question(message, parent=None):
   """The Question dialog, returns True if the user presses OK"""
   dialog = gtk.MessageDialog(flags=gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
                              type=gtk.MESSAGE_QUESTION,
                              buttons=gtk.BUTTONS_OK_CANCEL,
                              message_format=message)
   if parent != None: dialog.set_transient_for(parent)
   dialog.set_title(_("Question"))
   if dialog.run() == gtk.RESPONSE_OK:
      dialog.destroy()
      return True
   else:
      dialog.destroy()
      return False

def dialog_info(message, parent=None):
   """The Info dialog"""
   dialog = gtk.MessageDialog(flags=gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
                              type=gtk.MESSAGE_INFO,
                              buttons=gtk.BUTTONS_OK,
                              message_format=message)
   if parent != None: dialog.set_transient_for(parent)
   dialog.set_title(_("Info"))
   dialog.run()
   dialog.destroy()

def dialog_warning(message, parent=None):
   """The Warning dialog"""
   dialog = gtk.MessageDialog(flags=gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
                              type=gtk.MESSAGE_WARNING,
                              buttons=gtk.BUTTONS_OK,
                              message_format=message)
   if parent != None: dialog.set_transient_for(parent)
   dialog.set_title(_("Warning"))
   dialog.run()
   dialog.destroy()
   
def dialog_error(message, parent=None):
   """The Error dialog"""
   dialog = gtk.MessageDialog(flags=gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
                              type=gtk.MESSAGE_ERROR,
                              buttons=gtk.BUTTONS_OK,
                              message_format=message)
   if parent != None: dialog.set_transient_for(parent)
   dialog.set_title(_("Error"))
   dialog.run()
   dialog.destroy()

def set_bookmarks_menu_items(inst):
   """Set Bookmarks Menu Items"""
   bookmarks_menu = inst.ui.get_widget("/MenuBar/BookmarksMenu").get_submenu()
   for menu_item in inst.bookmarks_menu_items:
      bookmarks_menu.remove(menu_item)
   menu_item = gtk.SeparatorMenuItem()
   menu_item.show()
   bookmarks_menu.append(menu_item)
   inst.bookmarks_menu_items = [menu_item]
   for node_id_str in inst.bookmarks:
      if not long(node_id_str) in inst.nodes_names_dict: continue
      menu_item = gtk.ImageMenuItem(inst.nodes_names_dict[long(node_id_str)])
      menu_item.set_image(gtk.image_new_from_stock("gtk-open", gtk.ICON_SIZE_MENU))
      menu_item.connect("activate", select_bookmark_node, node_id_str, inst)
      menu_item.show()
      bookmarks_menu.append(menu_item)
      inst.bookmarks_menu_items.append(menu_item)

def set_recent_documents(inst):
   """Set Recent Documents Menu and Toolbar"""
   inst.recent_menu_1 = gtk.Menu()
   inst.recent_menu_2 = gtk.Menu()
   for target in [1, 2]:
      for filepath in inst.recent_docs:
         menu_item = gtk.ImageMenuItem(filepath)
         menu_item.set_image(gtk.image_new_from_stock("gtk-open", gtk.ICON_SIZE_MENU))
         menu_item.connect("activate", open_recent_document, filepath, inst)
         menu_item.show()
         if target == 1: inst.recent_menu_1.append(menu_item)
         else: inst.recent_menu_2.append(menu_item)
   # main menu
   recent_menuitem = gtk.ImageMenuItem(_("_Recent Documents"))
   recent_menuitem.set_image(gtk.image_new_from_stock("gtk-open", gtk.ICON_SIZE_MENU))
   recent_menuitem.set_tooltip_text(_("Open a Recent CherryTree Document"))
   recent_menuitem.set_submenu(inst.recent_menu_1)
   inst.ui.get_widget("/MenuBar/FileMenu").get_submenu().insert(recent_menuitem, 3)
   # toolbar
   menu_toolbutton = gtk.MenuToolButton("gtk-open")
   menu_toolbutton.set_tooltip_text(_("Open a CherryTree Document"))
   menu_toolbutton.set_arrow_tooltip_text(_("Open a Recent CherryTree Document"))
   menu_toolbutton.set_menu(inst.recent_menu_2)
   menu_toolbutton.connect("clicked", inst.file_open)
   inst.ui.get_widget("/ToolBar").insert(menu_toolbutton, 3)

def add_recent_document(inst, filepath):
   """Add a Recent Document if Needed"""
   if not filepath in inst.recent_docs:
      inst.recent_docs.append(filepath)
      for target in [1, 2]:
         menu_item = gtk.ImageMenuItem(filepath)
         menu_item.set_image(gtk.image_new_from_stock("gtk-open", gtk.ICON_SIZE_MENU))
         menu_item.connect("activate", open_recent_document, filepath, inst)
         menu_item.show()
         if target == 1: inst.recent_menu_1.append(menu_item)
         else: inst.recent_menu_2.append(menu_item)

def open_recent_document(menu_item, filepath, dad):
   """A Recent Document was Requested"""
   if os.path.isfile(filepath): dad.filepath_open(filepath)
   else:
      dialog_error(_("The Document %s was Not Found") % filepath, dad.window)
      menu_item.hide()
      try: dad.recent_docs.remove(filepath)
      except: pass

def select_bookmark_node(menu_item, node_id_str, dad):
   """Select a Node in the Bookmarks List"""
   node_iter = dad.get_tree_iter_from_node_id(long(node_id_str))
   if node_iter: dad.treeview_safe_set_cursor(node_iter)
