from sentence_transformers import SentenceTransformer
import numpy as np
import chromadb as DB


class VectorDatabase:
   def __init__(self, agent: str, embedding_model_name: str = 'all-MiniLM-L6-v2'):
       self.model = SentenceTransformer(embedding_model_name)
       self.client = DB.PersistentClient(path=agent)
       self.agent = agent
       self.memory = self.client.get_or_create_collection(name=self.agent)


   def get_id(self):
       return len(self.memory.get()['ids']) + 1


   def add(self, text: str, metadata: dict = None):

       embedding = self.model.encode(text)
       memory = self.client.get_collection(name=self.agent)
       memory.add(
           embeddings=[embedding],
           documents=[text],
           ids=[str(self.get_id())],
           metadatas=[metadata]
       )


   def search(self, query: str, top_k: int = 1):
       query_embedding = self.model.encode(query)
       results = self.memory.query(
           query_embeddings=[query_embedding],
           n_results=top_k,
           include=['documents', 'metadatas', 'distances']
       )
       return results


if __name__ == "__main__":
   memory_db = VectorDatabase(agent='AssistantMemory')

   memory_db.add("The sky is blue.", {"timestamp": "10:00PM", "source": "observation"})
   memory_db.add("The Ground is green.", {"timestamp": "11:00PM", "source": "observation"})
   print("Results1 bellow:")
   print(memory_db.search('blue'))
   results = memory_db.search('blue')
   first_doc = results['documents'][0][0]#https://www.w3schools.com/python/numpy/numpy_array_indexing.asp
   print("Results1 content bellow:")
   print(first_doc)
   print("Results2 bellow:")
   print(memory_db.search('green'))
