from ._anvil_designer import TeamFormTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class TeamForm(TeamFormTemplate):
  def __init__(self,row_Dict , **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties())
    
    # Any code you write here will run before the form opens.
    return_value = anvil.server.call('get_Players_OnTeam(1)')
    return_value = [{"SteamID" : r[0], "Name": r[1], "Playtime": r[2]} for r in return_value]
    self.RustTeam_repeating_panle.items = return_value
    print(return_value)
