import os, sys, datetime, tarfile, os.path
from pymongo import MongoClient
import subprocess
import shutil
import json

def get_folder_backup(dbname):
  dt = datetime.datetime.now()
  directory = ('backup_%s-%s-%s_%s_%s' % (dt.day,dt.month,dt.year, dt.hour, dt.minute))
  return directory

def run_backup(mongoUri, dbname):
  client = MongoClient(mongoUri)
  directory = get_folder_backup(dbname)
  print("--------------------------------------------")
  cmd= ('mongodump --uri="%s" -o %s/dump ' % (mongoUri,directory))
  print (subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True))
  return directory

def run_import(mongoUri, dbname):
  client = MongoClient(mongoUri)
  db = client[dbname]
  directory = get_folder_backup(dbname)
  os.chdir(directory)
  cmd="mongoresotre"
  # print subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)

if __name__ == '__main__':
  with open('config.json') as CONFIG_FILE:
    CONFIG = json.load(CONFIG_FILE)
    client = MongoClient(CONFIG['db']['url'])

  dbs_to_exclude = ['admin', 'config', 'local','test']
  directory = ''
  if (not(len(sys.argv) == 3) and not(len(sys.argv) == 2)):
    print('[-] Incorrect number of arguments')
    print('python run.py [dbname]')
    exit()
  else:
    host = CONFIG['db']['url']
    dbname = ""
    if ('--all' in sys.argv):
      for x in MongoClient().list_database_names():
        if (x not in dbs_to_exclude):
          mongoUri = ('%s/%s?authSource=admin&retryWrites=true&w=majority' % (host,x))
          try:
            directory = run_backup(mongoUri, x)
            print('[*] Successfully performed backup')
          except Exception as e:
            print('[-] An unexpected error has occurred')
            print('[-] '+ str(e) )
            print('[-] EXIT')
            print(MongoClient().list_database_names())
      for x in os.listdir():
        if(x.startswith('backup_')):
          shutil.move(x,'data')
    else:
      dbname = sys.argv[1]
      mongoUri = ('%s/%s?authSource=admin&retryWrites=true&w=majority' % (host,dbname))
      try:
        directory= run_backup(mongoUri, dbname)
        print('[*] Successfully performed backup')
      except Exception as e:
        print('[-] An unexpected error has occurred')
        print('[-] '+ str(e) )
        print('[-] EXIT')
      if(os.path.exists(directory)):
        shutil.move(directory,'data')

