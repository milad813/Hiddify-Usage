import pandas as pd
import sqlite3
import paramiko
import plotly.express as px
import secret
import subprocess



def check_interval():
    user_interval_choice = input("Please Select interval:\n1. per Day\n2. per hour\n")
    return 96 if user_interval_choice == "1" else 4

def import_database():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(secret.server_ip,port=4951 , username=secret.username, password=secret.password)
    sftp = ssh.open_sftp()
    sftp.get(secret.remote_path, secret.local_path)
    sftp.close()
    ssh.close()


def unpack_zip_file():
    subprocess.run(['powershell', '-Command', '&', '"C:/Program Files/7-Zip/7z.exe"', 'e', 'usage.db.xz', '-y'])

def create_dataframe():
    conn = sqlite3.connect(secret.local_path_db)
    sql_query = "SELECT * FROM user"
    df = pd.read_sql_query(sql_query, conn)
    conn.close()
    return df

def decrease_dataframe(df, interval):
    new_df = pd.DataFrame()
    for name in df["name"].unique():
        user_df = df[df["name"]==name]
        decreased_user_df = user_df.iloc[::interval]
        new_df = pd.concat([new_df,decreased_user_df])
    return new_df

def plot(dataframe):
    fig = px.line(dataframe, x="read_time", y="current_usage", color="name", markers=True)
    fig.show()


interval = check_interval()
import_database()
unpack_zip_file()
df = create_dataframe()
decreased_df = decrease_dataframe(df, interval)
plot(dataframe=decreased_df)
