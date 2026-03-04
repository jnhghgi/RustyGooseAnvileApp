import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import sqlite3


# Verbindung zur Datenbank (Die Datei muss in Anvil hochgeladen sein)
db_path = anvil.server.get_app_origin() + "/rust_final.db"


@anvil.server.callable
def get_team_stats():
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()
  cursor.execute("""
        SELECT Team.Name, COUNT(Player.SteamID) 
        FROM Team LEFT JOIN Player ON Team.TeamID = Player.TeamID 
        GROUP BY Team.Name
    """)
  return cursor.fetchall()


@anvil.server.callable
def get_resource_distribution():
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()
  cursor.execute("""
        SELECT Item.Name, SUM(Stores.amount) 
        FROM Item JOIN Stores ON Item.ItemID = Stores.ItemID 
        GROUP BY Item.Name
    """)
  return cursor.fetchall()

@anvil.server.callable
def get_all_players():
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()
  cursor.execute("SELECT Name, Playtime FROM Player ORDER BY Playtime DESC")
  return cursor.fetchall()

@anvil.server.callable
def get_all_teams():
  conn = sqlite3.connect(data_files["rust_final.db"])
  cursor = conn.cursor()
  cursor.execute("SELECT TeamID, Name FROM Team")
  return cursor.fetchall()
