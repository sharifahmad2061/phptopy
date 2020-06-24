import sqlite3
from datetime import datetime

# get data as command line arguments
card_uid = ''
device_token = ''

# todays date and time in United Kingdom Timezone
todays_date = datetime.strptime(datetime.now(), r"%Y-%m-%d")
nows_time = datetime.strptime(datetime.now(), r"%H:%M:%S%P")

# create database connection
conn = sqlite3.connect('rfidattendance')
cursor = conn.cursor()

if card_uid and device_token:
    device_uid = device_token
    sql = 'select * from devices where device_uid=?'
    try:
        cursor.execute(sql, (device_uid,))
        devices = cursor.fetchall()
        if len(devices):
            for device in devices:
                device_mode = device[-1]
                device_dep = device[2]
                if device_mode == 1:
                    users_sql = 'select * from users where card_uid=?'
                    cursor.execute(users_sql, (card_uid,))
                    users = cursor.fetchall()
                    if len(users):
                        # existing card used
                        # if row['add_card']  == 1
                        for user in users:
                            if user[-1] == 1:
                                # if ($row['device_uid'] == $device_uid ||
                                # $row['device_uid'] == 0)
                                if (user[-3] == device_uid) or (user[-3] == 0):
                                    user_name = user[1]
                                    serial_number = user[2]
                                    user_logs_sql = 'SELECT * FROM users_logs WHERE card_uid=? AND checkindate=? AND card_out=0'
                                    cursor.execute(
                                        user_logs_sql, (card_uid, todays_date))
                                    user_logs = cursor.fetchall()
                                    # login
                                    if len(user_logs):
                                        login_sql = """
                                                INSERT INTO users_logs
                                                    (username, serialnumber, card_uid, device_uid, device_dep, checkindate, timein, timeout)
                                                    VALUES (? ,?, ?, ?, ?, ?, ?, ?)"""
                                        timeout = "00:00:00"
                                        cursor.execute(
                                            login_sql,
                                            (user_name,
                                             serial_number,
                                             card_uid,
                                             device_uid,
                                             device_dep,
                                             todays_date,
                                             nows_time,
                                             timeout))
                                        conn.commit()
                                        print(f'login {username}')
                                    # logout
                                    else:
                                        logout_sql = "UPDATE users_logs SET timeout=?, card_out=1 WHERE card_uid=? AND checkindate=? AND card_out=0"
                                        cursor.execute(
                                            logout_sql, (nows_time, card_uid, todays_date))
                                        conn.commit()
                                        print(f'logout {user_name}')
                                else:
                                    # echo "Not Allowed!";
                                    print('Not Allowed')
                            elif user[-1] == 0:
                                print('not registered')
                    else:
                        print('Card Not found')
                elif device_mode == 0:
                    users_sql = "SELECT * FROM users WHERE card_uid=?"
                    cursor.execute(users_sql, (card_uid,))
                    users = cursor.fetchall()
                    if len(users):
                        # The card is available
                        card_select_sql = "SELECT card_select FROM users WHERE card_select=1"
                        cursor.execute(card_select_sql)
                        card_select_rows = cursor.fetchall()
                        if len(card_select_rows):
                            for card_select_row in card_select_rows:
                                sql = "UPDATE users SET card_select=0"
                                cursor.execute(sql)
                                conn.commit()
                                sql = "UPDATE users SET card_select=1 WHERE card_uid=?"
                                cursor.execute(sql, (card_uid,))
                                conn.commit()
                                print('available')
                        else:
                            sql = "UPDATE users SET card_select=1 WHERE card_uid=?"
                            cursor.execute(sql, (card_uid,))
                            conn.commit()
                            print("available")
                    else:
                        # the card is new
                        new_card_sql = "UPDATE users SET card_select=0"
                        cursor.execute(new_card_sql)
                        conn.commit()
                        new_user_sql = """
                            INSERT INTO users
                                (card_uid, card_select, device_uid, device_dep, user_date)
                                VALUES (?, 1, ?, ?, CURDATE())
                                """
                        cursor.execute(
                            new_user_sql, (card_uid, device_uid, device_dep))
                        conn.commit()
                        print("Successful")
                else:
                    print('Invalid Device Mode')
        else:
            print('Invalid Device')
    except Exception as exc:
        print(exc.__doc__)
