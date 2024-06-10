from connection.sql_server import get_connection

tableName = "T_TRN_LOG_DAILY"

def fetch_all_data():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT sum(total) as total FROM " + tableName)
        return cursor.fetchall()
