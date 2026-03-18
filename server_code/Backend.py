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
    query = "SELECT SteamID, Name, Playtime FROM Player WHERE TeamID = ?"
    cursor.execute(query, (TeamID,))
    return cursor.fetchall()


@anvil.server.callable
def get_team_experience_stats():
  with get_db_connection() as conn:
    cursor = conn.cursor()
    query = """
            SELECT T.Name, SUM(P.Playtime) as TotalHours 
            FROM Player P
            JOIN Team T ON P.TeamID = T.TeamID
            GROUP BY T.Name
            ORDER BY TotalHours
        """
    cursor.execute(query)
    rows = cursor.fetchall()
    teams = [f"Team {r[0]}" for r in rows]
    hours = [r[1] for r in rows]
    return teams, hours

@anvil.server.callable
def get_team_tc_counts():
  with get_db_connection() as conn:
    cursor = conn.cursor()
    query = """
            SELECT T.Name, COUNT(TC.TcID) as TCCount FROM Team T
            JOIN Tool_Cupboard TC ON T.TeamID = TC.TeamIDGROUP BY T.Name
            ORDER BY TCCount DESC"""
    cursor.execute(query)
    rows = cursor.fetchall()
    team_names = [r[0] for r in rows]
    tc_counts = [r[1] for r in rows]
    return team_names, tc_counts

@anvil.server.callable
def get_all_players():
  with get_db_connection() as conn:
    cursor = conn.cursor()
    # Fetching SteamID, Name, and Playtime from the Player table 
    cursor.execute("SELECT SteamID, Name FROM Player")
    return cursor.fetchall()



@anvil.server.callable
def get_all_player_bySteamID(SteamID):
  with get_db_connection() as conn:
    cursor = conn.cursor()
    # Fetching SteamID, Name, and Playtime from the Player table 
    cursor.execute("SELECT SteamID, Name FROM Player Where SteamID = ?",(SteamID,))
    return cursor.fetchall()

@anvil.server.callable
def get_team_name_by_steam_id(steam_id):
  with get_db_connection() as conn:
    cursor = conn.cursor()
    query = "SELECT T.Name, P.Playtime FROM Team T JOIN Player P ON T.TeamID = P.TeamID WHERE P.SteamID = ?"
    cursor.execute(query, (steam_id,))
    return cursor.fetchone()
