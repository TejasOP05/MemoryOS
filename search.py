from database import DatabaseManager


class SearchService:

    def __init__(self):

        self.db = DatabaseManager()

    def search(self, query):

        return self.db.search_files(query)