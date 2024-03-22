#!/usr/bin/python3
### This script will monitor and update file hashes in a MySQL database.
### DM-3122024

import os
import hashlib
import pymysql
import sys
from datetime import datetime

# MySQL database connection details
host = 'localhost'
user = 'cmdb'
password = 'Berouz1234!'
database = 'cmdb'
table = 'files'

# Main routine that is called when script is run
def main():
  """Get hash of file on cli and add to database"""
  # Get the file path
  if len(sys.argv) != 3:
    usage()
  else:
    myfile = sys.argv[2]

  # Check for correct command
  if sys.argv[1] != 'updatehash':
    usage()

  # Create file hash
  if not os.path.exists(myfile):
    print(myfile + ' does not exist')
    usage()

  filehash = get_hash(myfile)

  # Create a zulu timestamp
  timestamp = get_timestamp()

  # Connect to database
  db = pymysql.connect(host=host,user=user,password=passwd,database=database)
  cursor = db.cursor()

  # Verify the path is not already in the database.  If it is prompt if user
  # to see if they want to replace the has
  if path_exists(cursor, myfile ):
    ans = input('File path exists, do you want to overwrite (Y/N): ')
    if not ans == 'Y':
      exit('Exiting without any changes')
    else:
      delete_path(db,cursor,timestamp,myfile)

  # Now add the path
  add_path(db, cursor, timestamp,myfile,filehash)
  db.close()

# Subroutines
def path_exists(dbcursor, filepath):
  """ Check if path is already in the database """
  sql = "select * from files where path='"+filepath+"'"
  dbcursor.execute(sql)
  result = dbcursor.fetchall()
  if result == ():
    return 0
  else:
    return 1

def add_path(db, cursor, timestamp, myfile, filehash):
  """ Add hash to database """
  sql = "INSERT INTO files (timestamp, path, hash) VALUES ('%s','%s','%s')" % \
         (timestamp, myfile, filehash)

  # Run the sql statement rolling back if there is a problem
  try:
    cursor.execute(sql)
    db.commit()
  except Exception as e:
    db.rollback()
    print('Error with database insert:')
    print(e)

def delete_path(db, cursor, timestamp, myfile):
  """ Delete hash from database """
  sql = "DELETE FROM files where path='"+myfile+"'"

  # Run the sql statement rolling back if there is a problem
  try:
    cursor.execute(sql)
    db.commit()
  except Exception as e:
    db.rollback()
    print('Error with database delete:')
    print(e)

def get_hash(filepath):
  """ Create a hash of a file """
  md5 = hashlib.md5(open(filepath,'rb').read()).hexdigest()
  return(md5)

def get_timestamp():
  ts = datetime.now().isoformat()
  return(ts)

def usage():
  """ Usage information"""
  print('monitor1.py updatehash <filepath>')
  sys.exit()

# Run main() if script called directly, else use as a library to be imported
if __name__ == "__main__":
        main()

