#!/usr/bin/python3
import pandas as pd
import sqlite3
from datetime import datetime

import_conn = sqlite3.connect('/opt/hiddify-manager/hiddify-panel/hiddifypanel.db')
sql_query = 'SELECT name,last_online,current_usage_GB FROM user'
users_data = pd.read_sql_query(sql_query, import_conn)
users_data['read_time'] = datetime.now()
users_data['current_usage_GB'] = users_data['current_usage_GB'].round(2)
import_conn.close()

export_conn = sqlite3.connect('/home/usage.db')
users_data.to_sql('user', export_conn, index=False, if_exists='append', dtype={'last_online': 'DATETIME', 'current_usage_GB': 'NUMERIC'})
export_conn.close()