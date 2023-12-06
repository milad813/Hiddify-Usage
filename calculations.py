import pandas as pd
import sqlite3
import paramiko
import plotly.express as px
import secret


def import_database():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(secret.server_ip, username=secret.username, password=secret.password)
    sftp = ssh.open_sftp()
    sftp.get(secret.remote_path, secret.local_path)
    sftp.close()
    ssh.close()


def create_dataframe():
    conn = sqlite3.connect(secret.local_path)
    sql_query = "SELECT * FROM user"
    df = pd.read_sql_query(sql_query, conn)
    conn.close()
    return df


def user_dataframe(dataframe, username):
    return dataframe[dataframe["name"] == username]


def plot(dataframe):
    fig = px.line(dataframe, x="read_time", y="current_usage_GB", color="name")
    fig.show()


import_database()
df = create_dataframe()
plot(dataframe=df)
