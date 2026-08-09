"""
Pinecone Tool
Responsible for communicating with Pinecone.
Responsibilities:
- Connect to Pinecone
- Upsert vectors
- Query vectors
- Delete vectors
This tool performs NO AI reasoning.
"""
from typing import List, Dict, Any
from pinecone import Pinecone
from backend.config.settings import settings
from pinecone.exceptions import NotFoundException

class PineconeTool:
   
    def __init__(self):
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index = self.pc.Index(settings.PINECONE_INDEX_NAME)

    def upsert_vectors(self,vectors: List[Dict[str, Any]]) -> None: 
#Update if it exists, otherwise insert.
        self.index.upsert(vectors=vectors)



    def query_vectors(self,vector: List[float],top_k: int = 10,include_metadata: bool = True):
        """
        Retrieve similar vectors.
        """
        response = self.index.query(
            vector=vector,
            top_k=top_k,
            include_metadata=include_metadata,
        )
        return response.matches
    

    def delete_vectors(self,ids: List[str]):
        """
        Delete vectors by IDs.
        """
        self.index.delete(ids=ids)


    def delete_all(self):
        try:
            self.index.delete(delete_all=True)
        except Exception:
            raise ValueError("Nothing to delete")
    