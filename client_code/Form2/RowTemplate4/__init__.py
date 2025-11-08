from ._anvil_designer import RowTemplate4Template
from anvil import *
import anvil.server


class RowTemplate4(RowTemplate4Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
self.columns = [{"title":"A","data_key":"A"},{"title":"B","data_key":"B"}]
self.items = [{"A": 1, "B": 2}, {"A": 3, "B": 4}]
    # Any code you write here will run before the form opens.
