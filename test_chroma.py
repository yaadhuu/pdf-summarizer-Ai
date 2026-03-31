import chromadb
client = chromadb.Client()
try:
    client.create_collection("Test_PDF")
    print("Test_PDF successful")
except Exception as e:
    print("Error Test_PDF:", e)

try:
    client.create_collection("my_book(1)")
    print("my_book(1) successful")
except Exception as e:
    print("Error my_book(1):", e)
