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

  @handle("RustPlayers_Dashboard", "click")
  def RustPlayers_Dashboard_click(self, points, **event_args):
    """This method is called when a data point is clicked."""
    def refresh_chart(self):
      team_names, total_hours = anvil.server.call('get_team_experience_stats')
      self.plot_1.data = [
        go.Bar(
          x=team_names,
          y=total_hours,
          marker_color='#2196F3' # Optional: Rust-style blue or orange
        )
      ]

      # Add labels
      self.plot_1.layout.title = "Most Experienced Teams (Total Hours)"
      self.plot_1.layout.xaxis.title = "Team Name"
      self.plot_1.layout.yaxis.title = "Combined Playtime (Hours)"
