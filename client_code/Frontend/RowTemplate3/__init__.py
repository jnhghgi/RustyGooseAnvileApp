from ._anvil_designer import RowTemplate3Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate3(RowTemplate3Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  @handle("PlayerAuswaehl_Button", "click")
  def PlayerAuswaehl_Button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Frontend.PlayerForm', self.item)
