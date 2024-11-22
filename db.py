from langchain.vectorstores.chroma import Chroma
from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"  # Veritabanının dizini

def view_chroma_data():
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())
    data = db.get()  # Veritabanındaki tüm verileri alır
    print(f"Document IDs: {data['ids']}")
    print(f"Metadata: {data['metadatas']}")
    print(f"Documents: {data['documents']}")

if __name__ == "__main__":
    view_chroma_data()