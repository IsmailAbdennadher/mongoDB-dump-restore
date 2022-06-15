# mongoDB-dump-restore
This project includes Python scripts that dump/restore data from/to Mongo Atlas

#Requirements
To run scripts you may need to install:
- Python 3 : https://www.python.org/downloads
- MongoDB Tools: https://www.mongodb.com/try/download/database-tools
For further install instructions please visit :
  https://www.mongodb.com/docs/database-tools/installation/installation/
#Steps
- pip install pymongo
- (if needed) Edit config.json file by providing Mongo Atlas uri
### skip this step if you are using a linux OS
- Copy mongorestore.exe,mongodump.exe and mongoimport.exe from mongoDB tools directory in the same directory as scripts
#Run Script

### Run dump script
* if you want to import all databases:
`py backup.py --all`
* if you want to import a specific database:
`py backup.py [dbName]`
