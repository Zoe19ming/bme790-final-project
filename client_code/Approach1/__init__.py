from ._anvil_designer import Approach1Template
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.media
import anvil.users
from .RowTemplate import RowTemplateTemplate

class Approach1(Approach1Template):
  def __init__(self, **properties):
    self.init_components(**properties)
       # Keep __init__ light; actual population runs on show
    # (Designer expects a form_show or data_grid_1_show; we'll provide both)
  #Edited by Dec 4 Start

  def button_load_click(self, **event_args):
    uploaded_file = self.file_loader_app1.file
    resp = anvil.server.call('process_csv_file', uploaded_file)
    records = resp['records']
    columns = resp['columns']

    # tell the repeating panel which template to use and pass the columns in
    self.repeating_panel_1.item_template = RowTemplate.RowTemplate  # or RowTemplate if imported differently
    self.repeating_panel_1.item_template_args = {"columns": columns}

    # set the data (this creates one RowTemplate instance per record)
    self.repeating_panel_1.items = records
  #Finish
  
  def button_test_click(self, **event_args):
    """This method is called when the button is clicked"""
    try:
      res = anvil.server.call('ping')
      anvil.alert(f"ping -> {res}")
    except Exception as e:
      anvil.alert("Ping failed: " + str(e))
    pass
