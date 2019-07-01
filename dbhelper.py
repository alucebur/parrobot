"""
Class that lets us abstract the database management from our main code
"""
import sqlite3
import logging


class DBHelper:
    def __init__(self, db_name):
        """
        Connects to the given SQLite Database
            @db_name: name of the SQLite Database file
        """
        self.db_name = db_name
        try:
            self.conn = sqlite3.connect(db_name)
        except sqlite3.OperationalError:
            logging.critical("Connection could not be established.")

    def setup(self):
        """
        Creates the structure of the database the first time
        """
        stmt_table = """
            CREATE TABLE IF NOT EXISTS library (
                note_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                content TEXT
            )"""
        stmt_index = """ CREATE INDEX IF NOT EXISTS owner_index
                             ON library (user_id ASC)"""
        self.conn.execute(stmt_table)
        self.conn.execute(stmt_index)

    def add_item(self, user, item_text):
        """
        Adds a note to the database
            @user: chat_id, the author of the note
            @item_text: text in the note
        """
        stmt = "INSERT INTO library VALUES (NULL, ?, ?)"
        params = (user, item_text)
        self.conn.execute(stmt, params)
        self.conn.commit()

    def get_items(self, user):
        """
        Returns all the notes of a given author
            @user: chat_id, the author of the note
        """
        stmt = "SELECT note_id, content FROM library WHERE user_id=(?)"
        params = (user,)
        cur = self.conn.cursor()
        cur.execute(stmt, params)
        return cur.fetchall()

    def update_item(self, user, item_id, item_text):
        """
        Updates the given note with a new text
            @user: chat_id, the author of the note
            @item_id: identifier of the note in the database
            @item_text: text in the note
        """
        stmt = """ UPDATE library SET content=(?)
                    WHERE user_id=(?) AND note_id=(?)"""
        params = (item_text, user, item_id)
        self.conn.execute(stmt, params)
        self.conn.commit()

    def delete_item(self, user, item_id):
        """
        Deletes the given note from the database
            @user: chat_id, the author of the note
            @item_id: identifier of the note in the database
        """
        stmt = "DELETE FROM library WHERE user_id=(?) AND note_id=(?)"
        params = (user, item_id)
        self.conn.execute(stmt, params)
        self.conn.commit()
