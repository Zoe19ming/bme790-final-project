from ._anvil_designer import RowTemplateTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class RowTemplate(RowTemplateTemplate):
  def __init__(self, **properties):
    # properties automatically includes 'item' and will include 'columns'
    self.init_components(**properties)

    # `self.item` is the row dict, `self.columns` provided via item_template_args
    # clear existing children (defensive)
    self.flow_panel_1.clear()

    # add header/cell widgets for each column (131 of them)
    for col in getattr(self, "columns", []):
      # create a small label for the cell value (or use TextBox if you want editable)
      val = self.item.get(col, "")
      lbl = Label(text=str(val), tooltip=col)
      lbl.role = "data-cell"   # optional, for styling
      lbl.width = "120px"      # tweak: fixed width so layout is stable; or let it auto-size
      lbl.wrap = False
      self.flow_panel_1.add_component(lbl)