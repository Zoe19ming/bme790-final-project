# from ._anvil_designer import Approach21Template
# from anvil import *
# import anvil.server


# class Approach21(Approach21Template):

#   def __init__(self, **properties):
#     self.init_components(**properties)
#     # Store uploaded CSV file
#     self.clinical_file = None

#   def file_loader_clinical_change(self, file, **event_args):
#     """
#     Triggered when user selects a CSV file.
#     """
#     if file is None:
#       alert("No file selected. Please upload a CSV file.")
#       return

#     self.clinical_file = file
#     alert("File uploaded successfully.")

#   def button_run_analysis_click(self, **event_args):
#     """
#     Triggered when user clicks 'Start analysis'.
#     Calls the server, then displays all results
#     in the Demographic_characteristics DataGrid.
#     """
#     if self.clinical_file is None:
#       alert("Please upload the clinical CSV file first.")
#       return
  
#     # ---- BEFORE calling the server: show "running" status ----
#     self.button_run_analysis.enabled = False
#     self.label_status.text = "Running analysis, please wait..."
#     self.label_status.foreground = "blue"
  
#     try:
#       # Call server: get rows + sample sizes
#       result = anvil.server.call(
#         'analyze_dm_vs_non_dm',
#         self.clinical_file
#       )
  
#       rows = result["rows"]
#       n_dm = result["n_dm"]
#       n_non = result["n_non"]
      
#       self.repeating_panel_demographics.items = rows
  
#       cols = self.Demographic_characteristics.columns
#       cols[1]['title'] = f"DM_mean±SD (n={n_dm})"
#       cols[2]['title'] = f"NonDM_mean±SD (n={n_non})"
#       cols[3]['title'] = "p_value"
#       self.Demographic_characteristics.columns = cols
  
#       self.label_status.text = f"Analysis completed successfully. Metrics = {len(rows)}"
  
#     except Exception as e:
#       self.label_status.text = "Analysis failed. See error message."
#       alert(f"Error during analysis: {e}")
  
#     finally:
#       self.button_run_analysis.enabled = True


#   def returnhome_click(self, **event_args):
#     """This method is called when the button is clicked"""
#     open_form('Form1')
#     pass


from ._anvil_designer import Approach21Template
from anvil import *
import anvil.server


class Approach21(Approach21Template):

  def __init__(self, **properties):
    # Set up form and store uploaded clinical CSV
    self.init_components(**properties)
    self.clinical_file = None

  # ---------- File loader: upload CSV ----------
  def file_loader_clinical_change(self, file, **event_args):
    """
    Called when the user selects a CSV file.
    """
    if file is None:
      alert("No file selected. Please upload a CSV file.")
      return

    self.clinical_file = file
    alert("File uploaded successfully.")

  # ---------- Run analysis: call server, fill tables, show plots ----------
  def button_run_analysis_click(self, **event_args):
    """
    Called when the user clicks 'Start analysis'.

    Steps:
      1) Check that a CSV file has been uploaded
      2) Call the server function 'analyze_dm_vs_non_dm'
      3) Populate:
         - Demographic characteristics DataGrid
         - GM / WM / CSF / WMH tables (DataGrids)
         - GM / WM / CSF / WMH bar plots (Images)
    """
    if self.clinical_file is None:
      alert("Please upload the clinical CSV file first.")
      return

    # Update status label and disable the button during analysis
    self.button_run_analysis.enabled = False
    self.label_status.text = "Running analysis, please wait..."
    self.label_status.foreground = "blue"

    try:
      # 1) Call the server: this returns demographics + 4 domains
      result = anvil.server.call(
        'analyze_dm_vs_non_dm',
        self.clinical_file
      )

      # -------------------------------------------------
      # 2) Demographic/global comparison (existing table)
      # -------------------------------------------------
      rows = result["rows"]
      n_dm = result["n_dm"]
      n_non = result["n_non"]

      # Bind rows to the repeating panel inside the main DataGrid
      self.repeating_panel_demographics.items = rows

      # Update the DataGrid column headers to show sample sizes
      cols = self.Demographic_characteristics.columns
      # Column 0: Metric; column 1: DM; column 2: Non-DM; column 3: p_value
      cols[1]["title"] = f"DM_mean±SD (n={n_dm})"
      cols[2]["title"] = f"NonDM_mean±SD (n={n_non})"
      cols[3]["title"] = "p_value"
      self.Demographic_characteristics.columns = cols

      # -------------------------------------------------
      # 3) GM / WM / CSF / WMH tables
      #    (each DataGrid uses the same keys: metric, dm_mean_sd, non_dm_mean_sd, p_value)
      # -------------------------------------------------
      gm_rows = result.get("gm_rows", [])
      wm_rows = result.get("wm_rows", [])
      csf_rows = result.get("csf_rows", [])
      wmh_rows = result.get("wmh_rows", [])

      # Bind to the corresponding repeating panels
      # (you need to have these in the Designer)
      self.repeating_panel_gm.items = gm_rows
      self.repeating_panel_wm.items = wm_rows
      self.repeating_panel_csf.items = csf_rows
      self.repeating_panel_wmh.items = wmh_rows

      # -------------------------------------------------
      # 4) GM / WM / CSF / WMH bar plots (Images)
      # -------------------------------------------------
      gm_plot = result.get("gm_plot", None)
      if gm_plot is not None:
        self.image_gm.source = gm_plot

      wm_plot = result.get("wm_plot", None)
      if wm_plot is not None:
        self.image_wm.source = wm_plot

      csf_plot = result.get("csf_plot", None)
      if csf_plot is not None:
        self.image_csf.source = csf_plot

      wmh_plot = result.get("wmh_plot", None)
      if wmh_plot is not None:
        self.image_wmh.source = wmh_plot

      # -------------------------------------------------
      # 5) Final status
      # -------------------------------------------------
      self.label_status.text = (
        f"Analysis completed successfully. "
        f"Metrics (demographics/global) = {len(rows)}"
      )
      self.label_status.foreground = "green"

    except Exception as e:
      # If anything goes wrong, show an error and update status label
      self.label_status.text = "Analysis failed. See error message."
      self.label_status.foreground = "red"
      alert(f"Error during analysis: {e}")

    finally:
      # Always re-enable the button
      self.button_run_analysis.enabled = True

  # ---------- Navigation back to home ----------
  def returnhome_click(self, **event_args):
    """
    Called when the 'Home' button is clicked.
    """
    open_form('Form1')
