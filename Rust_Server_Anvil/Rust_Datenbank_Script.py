import sqlite3


def setup_and_fill_rust_db():
    # Verbindung herstellen
    conn = sqlite3.connect("rust_final.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    # --- 1. TABELLEN ERSTELLEN ---

    cursor.execute("DROP TABLE IF EXISTS learns;")
    cursor.execute("DROP TABLE IF EXISTS Stores;")
    cursor.execute("DROP TABLE IF EXISTS Blueprint;")
    cursor.execute("DROP TABLE IF EXISTS Item;")
    cursor.execute("DROP TABLE IF EXISTS Base;")
    cursor.execute("DROP TABLE IF EXISTS Tool_Cupboard;")
    cursor.execute("DROP TABLE IF EXISTS Player;")
    cursor.execute("DROP TABLE IF EXISTS Team;")

    cursor.execute("CREATE TABLE Team (TeamID INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT NOT NULL UNIQUE);")

    cursor.execute("""CREATE TABLE Player (
        SteamID INTEGER PRIMARY KEY, Name TEXT NOT NULL, Playtime REAL, TeamID INTEGER,
        FOREIGN KEY (TeamID) REFERENCES Team(TeamID) ON DELETE SET NULL);""")

    cursor.execute("""CREATE TABLE Tool_Cupboard (
        TcID INTEGER PRIMARY KEY AUTOINCREMENT, Upkeep DATETIME, TeamID INTEGER,
        FOREIGN KEY (TeamID) REFERENCES Team(TeamID) ON DELETE CASCADE);""")

    cursor.execute("""CREATE TABLE Base (
        BaseID INTEGER PRIMARY KEY AUTOINCREMENT, Coordinates TEXT, TcID INTEGER UNIQUE,
        FOREIGN KEY (TcID) REFERENCES Tool_Cupboard(TcID) ON DELETE CASCADE);""")

    cursor.execute(
        "CREATE TABLE Item (ItemID INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT NOT NULL, Stacksize INTEGER);")

    cursor.execute("""CREATE TABLE Blueprint (
        BpID INTEGER PRIMARY KEY AUTOINCREMENT, TechTier INTEGER, Cost INTEGER, ItemID INTEGER UNIQUE,
        FOREIGN KEY (ItemID) REFERENCES Item(ItemID) ON DELETE CASCADE);""")

    cursor.execute("""CREATE TABLE Stores (
        BaseID INTEGER, ItemID INTEGER, amount INTEGER NOT NULL,
        PRIMARY KEY (BaseID, ItemID),
        FOREIGN KEY (BaseID) REFERENCES Base(BaseID) ON DELETE CASCADE,
        FOREIGN KEY (ItemID) REFERENCES Item(ItemID) ON DELETE CASCADE);""")

    cursor.execute("""CREATE TABLE learns (
        SteamID INTEGER, BpID INTEGER,
        PRIMARY KEY (SteamID, BpID),
        FOREIGN KEY (SteamID) REFERENCES Player(SteamID) ON DELETE CASCADE,
        FOREIGN KEY (BpID) REFERENCES Blueprint(BpID) ON DELETE CASCADE);""")

    # --- 2. DATEN EINFÜGEN ---

    # Teams & Spieler
    teams = [('RUST-GODS',), ('Duo-Raiders',), ('Solo-Bunker',)]
    for t in teams:
        cursor.execute("INSERT INTO Team (Name) VALUES (?)", t)

    players = [
        (76561198001, 'Shadow', 1500, 1), (76561198002, 'PvP-God', 2000, 1),
        (76561198003, 'Lucky', 150, 2), (76561198004, 'Noob', 10, 2),
        (76561198005, 'LoneWolf', 5000, 3)
    ]
    cursor.executemany("INSERT INTO Player VALUES (?,?,?,?)", players)

    # Basen (Main, Raid-Base, Solo-Hütte)
    tcs = [('2026-03-05', 1), ('2026-03-01', 1), ('2026-03-04', 2), ('2026-03-10', 3)]
    for upkeep, t_id in tcs:
        cursor.execute("INSERT INTO Tool_Cupboard (Upkeep, TeamID) VALUES (?,?)", (upkeep, t_id))
        tc_id = cursor.lastrowid
        cursor.execute("INSERT INTO Base (Coordinates, TcID) VALUES (?,?)", (f"X:{tc_id * 10}, Y:{tc_id * 20}", tc_id))

    # Items & Blueprints (Die Liste aus dem letzten Schritt)
    item_list = [
        ('Assault Rifle', 1, 3, 500), ('Rocket', 10, 3, 500),
        ('Semi-Auto Rifle', 1, 2, 125), ('Medical Syringe', 2, 1, 75),
        ('Wood', 1000, 0, 0), ('Metal Fragments', 1000, 0, 0), ('Sulfur', 1000, 0, 0)
    ]

    for name, stack, tier, cost in item_list:
        cursor.execute("INSERT INTO Item (Name, Stacksize) VALUES (?,?)", (name, stack))
        item_id = cursor.lastrowid
        if tier > 0:
            cursor.execute("INSERT INTO Blueprint (TechTier, Cost, ItemID) VALUES (?,?,?)", (tier, cost, item_id))

    # Loot in Basen (Base 1 hat AKs und Schwefel, Base 4 hat viel Holz)
    loot = [(1, 1, 5), (1, 7, 10000), (4, 5, 25000)]
    cursor.executemany("INSERT INTO Stores VALUES (?,?,?)", loot)

    # Gelerntes Wissen (Shadow kennt AK und Spritzen)
    knowledge = [(76561198001, 1), (76561198001, 4), (76561198005, 1), (76561198005, 2)]
    cursor.executemany("INSERT INTO learns VALUES (?,?)", knowledge)

    conn.commit()
    conn.close()
    print("Rust-Datenbank wurde mit Teams, Basen und Items befüllt!")


if __name__ == "__main__":
    setup_and_fill_rust_db()