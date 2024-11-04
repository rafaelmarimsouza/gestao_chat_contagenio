import pandas as pd
import mysql.connector
from config import DB_CONFIG

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def load_description_options():
    conn = get_db_connection()
    query = "SELECT DISTINCT description FROM thread_types"
    df = pd.read_sql(query, conn)
    conn.close()
    return df['description'].tolist()

def load_data(start_date=None, end_date=None, user_app_hash=None, description=None):
    conn = get_db_connection()
    
    query = """
    SELECT m.thread_ID, m.created_at, m.role, m.text, t.user_app_hash, tt.description
    FROM messages m
    JOIN threads t ON m.thread_ID = t.id
    JOIN thread_types tt ON t.thread_type_id = tt.id
    WHERE 1=1
    """
    
    params = {}
    if start_date:
        query += " AND m.created_at >= %(start_date)s"
        params['start_date'] = start_date
    if end_date:
        query += " AND m.created_at <= %(end_date)s"
        params['end_date'] = end_date
    if user_app_hash:
        query += " AND t.user_app_hash = %(user_app_hash)s"
        params['user_app_hash'] = user_app_hash
    if description:
        query += " AND tt.description = %(description)s"
        params['description'] = description

    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df
