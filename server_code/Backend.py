import sqlite3
import anvil.server
from anvil.files import data_files

# Helper function to avoid repeating connection logic
def get_db_connection():
  # This is the correct way to access files uploaded to Data Files
  return sqlite3.connect(data_files['rust_final.db'])

@anvil.server.callable
def get_all_teams():
  with get_db_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT TeamID, Name FROM Team")
    return cursor.fetchall()

@anvil.server.callable
def get_team_stats():
  with get_db_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("""
            SELECT Team.Name, COUNT(Player.SteamID) 
            FROM Team LEFT JOIN Player ON Team.TeamID = Player.TeamID 
            GROUP BY Team.Name
        """)
    return cursor.fetchall()

@anvil.server.callable
def get_Players_OnTeam(TeamID):
  with get_db_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT SteamID, Name, Playtime FROM Player Where TeamID = TeamID")
    return cursor.fetchall()
