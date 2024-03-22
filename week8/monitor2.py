#!/usr/bin/env python3

import os
import sys
import time
import hashlib
import csv
from datetime import datetime
import pymysql

# Database connection details
DB_HOST = 'localhost'
DB_USER = 'cmdb'
DB_PASSWORD = 'Berouz1234!'
DB_NAME = 'cmdb'

# Main routine that is called when script is run
def main():
  """Get hash of file on cli and add to database"""
  # Connect to database
  db = pymysql.connect(host=host,user=user,password=passwd,database=database)
  cursor = db.cursor()

  # Get the file path
  if len(sys.argv) != 3:
    usage()
  
  # Handle the updatehash command
  if sys.argv[1] == 'updatehash':
    myfile = sys.argv[2]

    # Create a zulu timestamp
    timestamp = get_zulu_timestamp()
  
    # Create file hash
    if not os.path.exists(myfile):
      print(myfile + ' does not exist')
      usage()
  
    filehash = get_hash(myfile)
  
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

  # Handle the run command
  elif sys.argv[1] == 'run':
    mytime = int(sys.argv[2])
    sql = "select * from files"
    with open('monitorchecks.csv','a',newline='') as fout:
      # Write out the header row
      csvout = csv.writer(fout)
      csvout.writerow(['check date','check type','status','message'])

      # Infinite while loop
      while True:
        # Create a timestamp for when check is done
        timestamp = get_timestamp()
        
        # Get the files to check from the database
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
          hash_timestamp = row[0]
          filepath = row[1]
          dbhash = row[2]
          current_hash = get_hash(filepath)
          message = 'FILE='+filepath+', OLD_HASH='+dbhash+', OLD_HASH_DATE='+\
                    hash_timestamp+', CURRENT_HASH='+current_hash
          if current_hash == dbhash:
            status = 'OK'
          else:
            status = 'File Changed'
          csvout.writerow([timestamp,'filehash',status,message])

        # Force the buffer to write to the file
        fout.flush()

        # Wait mytime seconds and then do it again
        time.sleep(mytime)  


  # Handle all other cases
  else:
    usage()

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

def get_zulu_timestamp():
  ts = datetime.now().isoformat()
  return(ts)

def get_timestamp():
  ts = datetime.now().isoformat(timespec='seconds')
  return(ts)

def usage():
  """ Usage information"""
  print('monitor2.py updatehash <filepath>')
  print('monitor2.py run <time in seconds between runs>')
  sys.exit()

# Run main() if script called directly, else use as a library to be imported
if __name__ == "__main__":
        main()

