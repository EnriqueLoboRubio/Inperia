import sqlite3
import os

RUTA_DB = os.path.join(os.path.dirname(__file__), "database.db")

def obtener_conexion():
    conn = sqlite3.connect(RUTA_DB)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
