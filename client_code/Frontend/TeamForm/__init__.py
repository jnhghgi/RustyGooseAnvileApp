from ._anvil_designer import TeamFormTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class TeamForm(TeamFormTemplate):
  def __init__(self,row_Dict , **properties):
    self.init_components(**properties)
    return_value = anvil.server.call('get_Players_OnTeam', row_Dict['TeamID'])
    return_value = [{"SteamID": r[0], "Name": r[1], "Playtime": r[2]} for r in return_value]
    self.RustPlayer_Repeating_panel.items = return_value
    print(return_value)

  @handle("Home_Link", "click")
  def Home_Link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Frontend')

