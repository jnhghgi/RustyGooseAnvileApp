from ._anvil_designer import PlayerFormTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class PlayerForm(PlayerFormTemplate):
  def __init__(self,rowDict, **properties):
    self.row_dict = rowDict
    self.init_components(**properties)
    self.PlayerName_Label.text = rowDict["Name"]
    self.Main_content_panel.clear()
    # Any code you write here will run before the form opens.

  def Load_Blueprint_DataGrid(self):
    self.Main_content_panel.clear()
    self.Main_content_panel.add_component()
    
  def Load_PlayerStats_DataGrid(self):
    self.Main_content_panel.clear()
    TeamName, Playtime = anvil.server.call("get_team_name_by_steam_id", self.row_dict['SteamID'])
    self.RustPlayerStast_content_panel.items = [{"SteamID":self.row_dict['SteamID'],"Playtime": Playtime,"Team_Name": TeamName}]
    self.Main_content_panel.add_component(self.RustPlayerStats_DataGrid)
    
  @handle("Back_Link", "click")
  def Back_Link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Frontend')

  @handle("Blueprint_Link", "click")
  def Blueprint_Link_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  @handle("PlayerStats_Link", "click")
  def PlayerStats_Link_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.Load_PlayerStats_DataGrid()
