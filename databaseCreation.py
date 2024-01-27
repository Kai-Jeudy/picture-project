import sqlite3


def create_database():
    database = sqlite3.connect("image.db")
    cursor = database.cursor()

    # create main and backup image tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS image_table (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,data BLOB NOT NULL)
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS backup_image_table AS SELECT id, name, data FROM image_table
    """)

    database.commit()
    cursor.close()
    database.close()

