# from rag import RAGEngine

# rag = RAGEngine()

# while True:

#     question = input("\nAsk: ")

#     if question.lower() == "exit":

#         break

#     answer = rag.ask(question)

#     print("\nAnswer:")
#     print(answer)





from semantic_search import SemanticSearch

search = SemanticSearch()
while True:
    query = input("Search: ")

    results = search.search(query)

    for filename, path, text, score in results:
        # print("\n")
        print("FILE:", filename)
        print("PATH:", path)
        print("SCORE:", score)

        # print("\nPREVIEW:")
        # print(text[:200])

        print("-" * 50)
    if not results:
        print("No results found.")
        print('\n')
        continue