import sqlite3
from datetime import date
import actions

# Master password
password = "abc123"

# Request for password
print("--------------------------------------------------------------------")
print("You are trying to get access to a secure database.")

access = False
while access is not True:
    keyboard_entry = str(input("\nPlease enter the password: "))
    if keyboard_entry == 'q':
        break
    elif keyboard_entry == password:
        print('Access granted!\n')
        access = True

        # Set up a database connection
        conn = sqlite3.connect("secure_storage.db")
        cur = conn.cursor()
        try:
            cur.execute('''CREATE TABLE STORE
                (FILE_NAME TEXT PRIMARY KEY NOT NULL,
                FILE_TYPE TEXT NOT NULL,
                DATE_INSERTED TEXT NOT NULL,
                DATA TEXT);''')
            print("A safe space was created!")
            conn.commit()
        except:
            actions.show_database(conn)

        while True:
            print("\nWhich action would you like me to execute?")
            print("1: Open a file")
            print("2: Insert an item")
            print("3: Remove item")
            print("q: Exit storage space")
            action = str(input(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> "))
            if action == 'q':
                print("Exiting the database")
                break
            if action == '1':
                actions.open_file(conn, cur)
            if action == '2':
                actions.insert_item(date, conn, cur)
            if action == '3':
                actions.remove_item(conn, cur)
    else:
        print("Wrong password, access denied!")
        access = False
