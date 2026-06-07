from database import DatabaseManager

db = DatabaseManager()

results = db.keyword_search("sppu")

for row in results:
    print(row)