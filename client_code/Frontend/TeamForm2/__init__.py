from ._anvil_designer import TeamForm2Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objects as go


class TeamForm2(TeamForm2Template):
  def __init__(self,row_Dict, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.row_Dict = row_Dict
    self.TeamName_Label.text = row_Dict['Name']
    # Any code you write here will run before the form opens.
    self.Main_content_panel.clear()
    self.Load_RustTeam_DataGrid()

  def Load_RustTeam_DataGrid(self):
    self.Main_content_panel.clear()
    return_value = anvil.server.call('get_Players_OnTeam', self.row_Dict['TeamID'])
    return_value = [{"SteamID": r[0], "Name": r[1], "Playtime": r[2]} for r in return_value]
    self.RustPlayer_Repeating_panel.items = return_value
    self.Main_content_panel.add_component(self.RustTeam_Members_DataGrid)

  def Load_BaseMap_Dashboard(self):
    self.Main_content_panel.clear()
    all_bases = anvil.server.call('get_base_locations')
    plot = anvil.Plot()
    teams = list(set([b['team'] for b in all_bases]))
    traces = []
    for team in teams:
      team_bases = [b for b in all_bases if b['team'] == team]
      traces.append(
        go.Scatter(x=[b['x'] for b in team_bases],y=[b['y'] for b in team_bases],
          mode='markers+text',name=team, marker=dict(size=12),
          text=[b['team'] for b in team_bases], textposition="top center"
        )
      )
    plot.data = traces
    plot.layout.title = "Server Base Map (Top-Down)"
    plot.layout.xaxis.title = "X Coordinate"
    plot.layout.yaxis.title = "Y Coordinate"
    plot.layout.width = 600
    plot.layout.height = 600
    self.Main_content_panel.add_component(plot)
    
  def Load_TeamItems_DataGrid(self):
    self.Main_content_panel.clear()
    return_value = anvil.server.call('get_team_inventory', self.row_Dict['TeamID'])
    return_value = [{"Name": r[0], "Amount": r[1]} for r in return_value]
    self.RustItem_repeating_panel.items = return_value
    self.Main_content_panel.add_component(self.RustItem_DataGrid)
  
  @handle("Back_Link", "click")
  def Back_Link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Frontend')

  @handle("TeamItems", "click")
  def TeamItems_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.Load_TeamItems_DataGrid()

  @handle("Bases_Link", "click")
  def Bases_Link_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.Load_BaseMap_Dashboard()

  @handle("TeamMembers_Link", "click")
  def TeamMembers_Link_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.Load_RustTeam_DataGrid()
