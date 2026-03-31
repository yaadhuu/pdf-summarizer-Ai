import chromadb
client = chromadb.Client()
print(type(client.list_collections()))
if len(client.list_collections()) > 0:
    print(type(client.list_collections()[0]))
