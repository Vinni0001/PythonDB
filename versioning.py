import os
import re
import time

try:
    with open ("./1.0_create_library_db.py") as startup:
        exec(startup.read())   
except:
    with open ("./db_create_creds.py") as f:
        exec(f.read())     

    mycursor = mydb.cursor(prepared = True) #COMMUNICATES WITH ENTIRE SERVER

    def create_db ():
        mycursor.execute("CREATE DATABASE IF NOT EXISTS library") #creates db
        mycursor.execute("SHOW DATABASES") #obtains list of all dbs

    #for x in mycursor: #lists all dbs
    #    print(x)

    create_db()

with open ("./creds.py") as creds:
    exec(creds.read())   

mycursor = mydb.cursor() #COMMUNICATES WITH ENTIRE SERVER


def itr_dir():
    global dir_list
    global cwd
    global filename_list

    dir_list = []
    filename_list = []
    # assign directory
    cwd = os.chdir("./Scripts")  # Get the current working directory (cwd)
 
    # iterate over files in that directory
    for filename in os.listdir(cwd):
        f = filename
    # checking if it is a file
        if os.path.isfile(f):
            filename_list.append(f)
            f = re.sub("[^\d.]","",f)
            f = f[:-1]
            if f == '':
                pass
            else:
                dir_list.append(float(f))
        else: 
            pass
    
    filename_list.sort()
    dir_list.sort()
    print(filename_list, dir_list)


def last_rec_db():
    global last_rec
    global latest_ver

    #Check to see if db exists, if not, run all scripts (create db, tables, etc), then add versions to db once created
    query = """SHOW TABLES LIKE 'VersionHistory'""" #Queries whether db is a table
    mycursor.execute(query)
    VH_exists_check = mycursor.fetchone() #Push output into variable
    print(VH_exists_check)

    if VH_exists_check == None: #If var is none, need to run all scripts.
        for i in range(0, len(dir_list)):
             
            if os.path.isfile(filename_list[i]) and i > 0: # checking if it is a file

                with open (f"./{filename_list[i]}") as filename:
                    exec(filename.read())

                query = """Select version from VersionHistory where version = '1.0'""" #Queries whether db is a table
                mycursor.execute(query)
                create_db_exists_check = mycursor.fetchone()

                if create_db_exists_check == None:
                    insert_create_db_ver =  """INSERT INTO VersionHistory (version, date) VALUES (%s, now())"""
                    mycursor.execute(insert_create_db_ver, [dir_list[0]])
                else:
                    pass
                print(i, os.getcwd(), create_db_exists_check)
                #time.sleep(1)

                add_ver = dir_list[i]
                print(add_ver)
                insert_ver =  """INSERT INTO VersionHistory (version, date) VALUES (%s, now())"""
                mycursor.execute(insert_ver, [add_ver])
            
            mydb.commit()
            time.sleep(1)

    else:
        query = """SELECT version FROM VersionHistory ORDER BY ID DESC LIMIT 1"""
        mycursor.execute(query)
        last_rec = mycursor.fetchone()
   
        if last_rec:
            #get_ver = """SELECT version FROM VersionHistory ORDER BY ID DESC LIMIT 1"""
            #mycursor.execute(get_ver)
            latest_ver = str(last_rec)
            latest_ver = [float(num) for num in re.findall(r'[\d.]+', latest_ver)]

            if max(dir_list) > latest_ver[0]:
                insert_ver =  """INSERT INTO VersionHistory (version, date) VALUES (%s, now())"""
                val = max(dir_list)
                mycursor.execute(insert_ver, [val])

            mydb.commit()
            mydb.close()
        else:
            pass

    mydb.close()

itr_dir()
last_rec_db()

  
