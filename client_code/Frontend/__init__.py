from ._anvil_designer import FrontendTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Frontend(FrontendTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    return_value = anvil.server.call('get_all_teams')
    return_value = [{"TeamID" : r[0], "Name": r[1]} for r in return_value]
    self.RustTeam_repeating_panle.items = return_value
    print(return_value)
