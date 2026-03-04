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
    return_value = anvil.server.call('query_database','SELECt name FROM gefaengnis')
    return_value = [entry["gefaengnis_name"] for entry in return_value]
    self.drop_down_gefaengnisliste.items = return_value
    print(return_value)
