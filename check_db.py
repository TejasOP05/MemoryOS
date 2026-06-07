from database import DatabaseManager

db = DatabaseManager()

files = db.get_all_files()

for file in files:
    print(file)
    
print("Done")
db.close()


