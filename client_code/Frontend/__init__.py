from ._anvil_designer import FrontendTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Frontend(FrontendTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.Main_FlowPanel.clear()

  def Load_TeamOverview_Datagrid(self):
    self.Main_FlowPanel.clear()
    return_value = anvil.server.call('get_all_teams')
    return_value = [{"TeamID" : r[0], "Name": r[1]} for r in return_value]
    self.RustTeam_repeating_panle.items = return_value
    self.Main_FlowPanel.add_component(self.RustTeam_DataGrid)

  def Load_PlayerExperience_Dashboard(self):
    self.Main_FlowPanel.clear()
    team_names, total_hours = anvil.server.call('get_team_experience_stats')
    plot = anvil.Plot()
    plot.data = [go.Bar(x=team_names,y=total_hours,marker_color='#C08497')]
    plot.layout.title = "Team Experience Leaderboard"
    plot.layout.xaxis.title = "Team Name"
    plot.layout.yaxis.title = "Total Playtime(Hours)"
    self.Main_FlowPanel.add_component(plot)

    import plotly.graph_objects as go

  def Load_TC_Ownership_Dashboard(self):
    self.Main_FlowPanel.clear()
    names, counts = anvil.server.call('get_team_tc_counts')
    plot = anvil.Plot()
    plot.data = [
      go.Bar(
        x=names,
        y=counts,
        marker_color='#4CAF50',
        text=counts,           
        textposition='auto'
      )
    ]
    plot.layout.title = "Tool Cupboard Distribution by Team"
    plot.layout.xaxis.title = "Team Name"
    plot.layout.yaxis.title = "Number of TCs Owned"
    plot.layout.yaxis.dtick = 1
    self.Main_FlowPanel.add_component(plot)

  @handle("PlayerHours_Plot", "click")
  def PlayerHours_Plot_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.Load_PlayerExperience_Dashboard()

  @handle("TeamOverview_Datagrid", "click")
  def TeamOverview_Datagrid_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.Load_TeamOverview_Datagrid()

  @handle("TC_Ranking", "click")
  def TC_Ranking_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.Load_TC_Ownership_Dashboard()

  


    