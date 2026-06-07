from search import SearchService

search = SearchService()

query = input("Enter search query: ")

results = search.search(query)

for filename, path, content in results:

    print("\n")
    print(filename)
    print(path)

    # print(content[:300])

    print("-" * 50)