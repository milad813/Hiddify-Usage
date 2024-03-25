#!/usr/bin/python3
import pandas as pd
import sqlite3
from datetime import datetime
import mysql.connector
import secret

def retrieve_data():
    conn = mysql.connector.connect(
            host='localhost',
            user=secret.username,
            password=secret.password,
            database='hiddifypanel'
        )
    cursor = conn.cursor()
    cursor.execute("SELECT name, current_usage FROM user")
    rows = cursor.fetchall()

    columns = ["name", "current_usage"]
    users_data = pd.DataFrame(rows, columns=columns)
    users_data["read_time"] = datetime.now()
    users_data["current_usage"] = users_data["current_usage"].round(2)
    cursor.close()
    conn.close()
    return users_data


def export_data(users_data):
    export_conn = sqlite3.connect("/root/usage.db")
    users_data.to_sql(
        "user",
        export_conn,
        index=False,
        if_exists="append",
        dtype={"current_usage": "NUMERIC"},
    )
    export_conn.close()


users_data = retrieve_data()
export_data(users_data)