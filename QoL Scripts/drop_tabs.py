with open ("creds.py") as f:
    exec(f.read())   

mycursor = mydb.cursor() #COMMUNICATES WITH ENTIRE SERVER

def drop_rel_tabs ():
  mycursor.execute("DROP TABLE IF EXISTS book_order")
  mycursor.execute("DROP TABLE IF EXISTS book_author")
  mycursor.execute("DROP TABLE IF EXISTS book_genre")

def drop_tabs ():
  mycursor.execute("DROP TABLE IF EXISTS orders")
  mycursor.execute("DROP TABLE IF EXISTS customers")
  mycursor.execute("DROP TABLE IF EXISTS books")
  mycursor.execute("DROP TABLE IF EXISTS authors")
  mycursor.execute("DROP TABLE IF EXISTS genre")
  mycursor.execute("DROP TABLE IF EXISTS VersionHistory")

  mycursor.execute("SHOW TABLES")

  for x in mycursor: #lists all dbs
    print(x)

drop_rel_tabs()
drop_tabs()