import pickle



with open('data/chunk_map.pkl', 'rb') as f:
    loaded = pickle.load(f)
print(loaded)