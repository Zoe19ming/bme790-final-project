from ._anvil_designer import RowTemplate3Template
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class RowTemplate3(RowTemplate3Template):
  def __init__(self, item=None, **properties):
    """
        item: a dict representing one row (keys -> values)
        """
    # standard init
    self.init_components(**properties)

    # Clear container (safety)
    self.container_panel.clear()

    if not item:
      return

      # Render each key/value as two labels (key: value).
      # You can change layout here; this uses one horizontal FlowPanel per column.
    for k, v in item.items():
      # Create a FlowPanel to hold key + value horizontally
      row_panel = anvil.FlowPanel()
      row_panel.role = "row"  # optional, for styling

      # Key label (small / bold)
      key_label = anvil.Label(text=str(k) + ":")
      key_label.font_weight = "bold"
      key_label.role = "key_label"
      key_label.set_event_handler('click', lambda **e: None)  # avoid warnings

      # Value — choose TextBox/TextArea for long text, else Label
      # Convert lists/dicts to string for display. Customize formatting as needed.
      if isinstance(v, (list, dict)):
        val_text = str(v)
        val_comp = anvil.TextArea(text=val_text, readonly=True)
        val_comp.rows = 2
      else:
        val_comp = anvil.Label(text=str(v))
        val_comp.role = "value_label"

        # Optional spacing style
      key_label.padding = "6px"
      val_comp.padding = "6px"

      # Add them to the row panel, then add row panel to container
      row_panel.add_component(key_label)
      row_panel.add_component(val_comp)

      self.container_panel.add_component(row_panel)
