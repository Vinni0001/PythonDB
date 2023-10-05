with open ("db_create_creds.py") as f:
    exec(f.read())     

mycursor = mydb.cursor() #COMMUNICATES WITH ENTIRE SERVER

def create_db ():
  mycursor.execute("CREATE DATABASE IF NOT EXISTS library") #creates db
  mycursor.execute("SHOW DATABASES") #obtains list of all dbs

  for x in mycursor: #lists all dbs
    print(x)


create_db()
