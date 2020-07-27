import pandas as pd
import base64

def show_database(conn):
    print("These are what you have in the database thus far: ")
    print("--------------------------------------------------")
    df = pd.read_sql_query("SELECT FILE_NAME, FILE_TYPE, DATE_INSERTED FROM STORE ORDER BY DATE_INSERTED", conn)
    print(df)
    print("--------------------------------------------------")
    return

def open_file(conn, cur):
    file_name = input('Which file would you like to open? ')
    # Checks if such file exists in the database
    df = pd.read_sql_query(" SELECT * FROM STORE WHERE FILE_NAME = '%s';" %file_name, conn)
    if df.empty:
        print("This file does not exist!")
    else:
        file_name = df.iloc[0,0]
        file_type = df.iloc[0,1]
        data = df.iloc[0,-1]

        with open(r'.\\%s.%s' %(file_name,file_type),'wb') as f:

            base64_bytes = data.encode('ascii')
            message_bytes = base64.b64decode(base64_bytes)
            # message = message_bytes.decode('ascii')
            f.write(message_bytes)

def insert_item(date, conn, cur):
    file_path = input("Drag in file you want to store for safe keeping: ")

    # Extracting file data
    data = ""
    with open(r'%s' %file_path,'rb') as f:
        data = f.read()
        print(type(data))
        # data_bytes = data.encode('ascii')
        base64_encoded = base64.b64encode(data)
        data_base64 = base64_encoded.decode('ascii')

    date_inserted = date.today().isoformat()
    # path = (file_path)
    file_path = file_path.split("\\")[-1].rstrip("\"")
    file_name = file_path.split(".")[0]
    file_type = file_path.split(".")[-1]
    # Insert into database
    with conn:
        command = "INSERT INTO STORE VALUES (\'%s\', \'%s\', \'%s\',  \'%s\');" %(file_name, file_type, date_inserted, data_base64)
        cur.execute(command)
        conn.commit()
    print("File has been sucessfully stored in the database")
    show_database(conn)
    return

def remove_item(conn, cur):
    file_name = input("Which file would you like to remove? ")

    # Checks if such file exists in the database
    df = pd.read_sql_query(" SELECT * FROM STORE WHERE FILE_NAME = '%s';" %file_name, conn)
    if df.empty:
        print("This file does not exist!")
    else:
        # Additional confirmation for the deletion
        flag = True
        while flag:
            response = input("Are you sure you want to remove this file? Y/N\n")
            response = str(response).upper()
            if response == "Y":
                flag = False
                with conn:
                    command = "DELETE FROM STORE WHERE FILE_NAME = \'%s\';" %file_name
                    cur.execute(command)
                    conn.commit()
                print("The file has been removed from the database:")
                show_database(conn)
            elif response == "N":
                flag = False
                break
            else:
                print("Invalid input!\n")
                break

srg = "perter"
srg.encode('ascii')
