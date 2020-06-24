import sys
from datetime import datetime, timezone, timedelta
import configparser
import argparse

import mysql.connector as mc
from dateutil.tz import gettz

# get data as command line arguments
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('card_uid', help="card identification to use for login")
arg_parser.add_argument('device_token', help="device that is used for authentication")
args = arg_parser.parse_args()

card_uid = args.card_uid
device_token = args.device_token
# print(card_uid, device_token)


# read configurations
parser = configparser.ConfigParser()
parser.read("config.cfg")
host = parser['DEFAULT']['DbHost']
db = parser['DEFAULT']['Database']
user = parser['DEFAULT']['User']
password = parser['DEFAULT']['Password']

# print(host, db, user, password)

# todays date and time in United Kingdom Timezone
london_tz = gettz('Europe/London')
londom_timedelta = london_tz.utcoffset(datetime.now(timezone.utc))
todays_date = datetime.strftime(datetime.now(timezone.utc) + londom_timedelta, r"%Y-%m-%d")
nows_time = datetime.strftime(datetime.now(timezone.utc) + londom_timedelta, r"%H:%M:%S%P")
# print(todays_date)
# print(nows_time)

# create database connection
try:
    conn = mc.connect(user=user, password=password, host=host, database=db)
    cursor = conn.cursor(prepared=True)
except mc.Error as err:
  if err.errno == mc.errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == mc.errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
    if card_uid and device_token:
        device_uid = device_token
        sql = 'select * from devices where device_uid=?'
        try:
            cursor.execute(sql, (device_uid,))
            devices = cursor.fetchall()
            # if a device with the specific device uid is found
            if len(devices):
                for device in devices:
                    device_mode = device[-1]
                    device_dep = device[2]
                    # device mode 1
                    if device_mode == 1:
                        users_sql = 'select * from users where card_uid=?'
                        try:
                            cursor.execute(users_sql, (card_uid,))
                        except mc.Error as err:
                            print(f'users table error -> {err}')
                            cursor.close()
                            conn.close()
                            exit(1)
                        users = cursor.fetchall()
                        # if the card belongs to a known user
                        if len(users):
                            # existing card used
                            # if row['add_card']  == 1
                            for user in users:
                                # if column add_card is 1
                                if user[-1] == 1:
                                    # if ($row['device_uid'] == $device_uid ||
                                    # $row['device_uid'] == 0)
                                    if (user[-3] == device_uid) or (user[-3] == 0):
                                        # grab username and serialnumber to a variable
                                        user_name = user[1]
                                        serial_number = user[2]
                                        user_logs_sql = 'SELECT * FROM users_logs WHERE card_uid=? AND checkindate=? AND card_out=0'
                                        try:
                                            cursor.execute(
                                                user_logs_sql, (card_uid, todays_date))
                                        except mc.Error as err:
                                            print(f'user_logs table error -> {err}')
                                            cursor.close()
                                            conn.close()
                                            exit(1)
                                        user_logs = cursor.fetchall()
                                        # login
                                        if len(user_logs):
                                            login_sql = """
                                                    INSERT INTO users_logs
                                                        (username, serialnumber, card_uid, device_uid, device_dep, checkindate, timein, timeout)
                                                        VALUES (? ,?, ?, ?, ?, ?, ?, ?)"""
                                            timeout = "00:00:00"
                                            try:
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
                                            except mc.Error as err:
                                                print(f'error inserting into user_logs table -> {err}')
                                                cursor.close()
                                                conn.close()
                                                exit(1)
                                            conn.commit()
                                            print(f'login {user_name}')
                                        # logout
                                        else:
                                            logout_sql = "UPDATE users_logs SET timeout=?, card_out=1 WHERE card_uid=? AND checkindate=? AND card_out=0"
                                            try:
                                                cursor.execute(
                                                    logout_sql, (nows_time, card_uid, todays_date))
                                            except mc.Error as err:
                                                print('error while logging a user out -> {err}')
                                                cursor.close()
                                                conn.close()
                                                exit(1)
                                            conn.commit()
                                            print(f'logout {user_name}')
                                    # either device_uid is not 0 or is not equal to commandline arg device_uid
                                    else:
                                        # echo "Not Allowed!";
                                        print('Not Allowed')
                                        cursor.close()
                                        conn.close()
                                        exit(1)
                                # if column add_card is 0
                                elif user[-1] == 0:
                                    print('not registered')
                                    cursor.close()
                                    conn.close()
                                    exit(1)
                        # card is not known
                        else:
                            print('Card Not found')
                            cursor.close()
                            conn.close()
                            exit(1)
                    # device mode 0
                    elif device_mode == 0:
                        users_sql = "SELECT * FROM users WHERE card_uid=?"
                        try:
                            cursor.execute(users_sql, (card_uid,))
                        except mc.Error as err:
                            print(f'users table error -> {err}')
                            cursor.close()
                            conn.close()
                            exit(1)
                        users = cursor.fetchall()
                        # The card is available
                        if len(users):
                            card_select_sql = "SELECT card_select FROM users WHERE card_select=1"
                            try:
                                cursor.execute(card_select_sql)
                            except mc.Error as err:
                                print(f'card_select col from users error -> {err}')
                                cursor.close()
                                conn.close()
                                exit(1)
                            card_select_rows = cursor.fetchall()
                            if len(card_select_rows):
                                for card_select_row in card_select_rows:
                                    sql = "UPDATE users SET card_select=0"
                                    try:
                                        cursor.execute(sql)
                                    except mc.Error as err:
                                        print(f'card_select=0 -> {err}')
                                        cursor.close()
                                        conn.close()
                                        exit(1)
                                    conn.commit()
                                    sql = "UPDATE users SET card_select=1 WHERE card_uid=?"
                                    try:
                                        cursor.execute(sql, (card_uid,))
                                    except mc.Error as err:
                                        print(f'card_select=1 -> {err}')
                                        cursor.close()
                                        conn.close()
                                        exit(1)
                                    conn.commit()
                                    print('available')
                            else:
                                sql = "UPDATE users SET card_select=1 WHERE card_uid=?"
                                try:
                                    cursor.execute(sql, (card_uid,))
                                except mc.Error as err:
                                    print(f'card_select=1 -> {err}')
                                    cursor.close()
                                    conn.close()
                                    exit(1)
                                conn.commit()
                                print("available")
                        else:
                            # the card is new
                            new_card_sql = "UPDATE users SET card_select=0"
                            try:
                                cursor.execute(new_card_sql)
                            except mc.Error as err:
                                print(f'card_select=0 -> {err}')
                                cursor.close()
                                conn.close()
                                exit(1)
                            conn.commit()
                            new_user_sql = """
                                INSERT INTO users
                                    (card_uid, card_select, device_uid, device_dep, user_date)
                                    VALUES (?, 1, ?, ?, CURDATE())
                                    """
                            try:
                                cursor.execute(
                                    new_user_sql, (card_uid, device_uid, device_dep))
                            except mc.Error as err:
                                print(f'new user error -> {err}')
                                cursor.close()
                                conn.close()
                                exit(1)
                            conn.commit()
                            print("Successful")
                    # invalid device mode
            # no device with the specified device uid is found
            else:
                print('Invalid Device')
        except mc.Error as err:
            print(f'devices table error -> {err}')
    else:
        print("No arguments provided")
    cursor.close()
    conn.close()