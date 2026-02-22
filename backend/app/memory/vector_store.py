import os
import chromadb
from chromadb.config import Settings
from app.config import settings
from app.utils.logger import get_logger
from app.utils.exceptions import VectorStoreException
from typing import List, Dict, Any, Optional
import uuid
import json
import numpy as np

logger = get_logger(__name__)

os.environ["ANONYMIZED_TELEMETRY"] = "False"

class VectorStore:
    def __init__(self):
        """Initialize vector store with ChromaDB"""
        try:
            # Disable telemetry
            self.client = chromadb.PersistentClient(
                path=settings.VECTOR_DB_PATH,
                settings=Settings(anonymized_telemetry=False)
            )
            self.collections = {}
            logger.info(f"Vector store initialized at {settings.VECTOR_DB_PATH}")
        except Exception as e:
            logger.error(f"Failed to initialize vector store: {str(e)}")
            # Create a dummy client if ChromaDB fails
            self.client = None
            self.collections = {}
    
    def get_or_create_collection(self, name: str):
        """Get or create a collection"""
        try:
            if name not in self.collections:
                self.collections[name] = self.client.get_or_create_collection(
                    name=name,
                    metadata={"hnsw:space": "cosine"}
                )
            return self.collections[name]
        except Exception as e:
            logger.error(f"Collection error: {str(e)}")
            raise VectorStoreException(f"Failed to get/create collection {name}: {str(e)}")
    
    async def add_document(
        self,
        collection_name: str,
        document: str,
        embedding: List[float],
        metadata: Optional[Dict[str, Any]] = None,
        doc_id: Optional[str] = None
    ):
        """Add document to vector store"""
        try:
            collection = self.get_or_create_collection(collection_name)
            
            if doc_id is None:
                doc_id = str(uuid.uuid4())
            
            # Ensure embedding is list of floats
            if isinstance(embedding, np.ndarray):
                embedding = embedding.tolist()
            
            collection.add(
                embeddings=[embedding],
                documents=[document],
                metadatas=[metadata or {}],
                ids=[doc_id]
            )
            
            logger.info(f"Added document to {collection_name} with ID: {doc_id}")
            return doc_id
            
        except Exception as e:
            logger.error(f"Add document error: {str(e)}")
            raise VectorStoreException(f"Failed to add document: {str(e)}")
    
    async def add_documents_batch(
        self,
        collection_name: str,
        documents: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[Dict]] = None,
        ids: Optional[List[str]] = None
    ):
        """Add multiple documents in batch"""
        try:
            collection = self.get_or_create_collection(collection_name)
            
            if ids is None:
                ids = [str(uuid.uuid4()) for _ in documents]
            
            if metadatas is None:
                metadatas = [{} for _ in documents]
            
            # Convert numpy arrays to lists
            embeddings = [e.tolist() if isinstance(e, np.ndarray) else e for e in embeddings]
            
            collection.add(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Added {len(documents)} documents to {collection_name}")
            return ids
            
        except Exception as e:
            logger.error(f"Batch add error: {str(e)}")
            raise VectorStoreException(f"Failed to add documents batch: {str(e)}")
    
    async def search_similar(
        self,
        collection_name: str,
        query_embedding: List[float],
        n_results: int = 5,
        filter_criteria: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """Search similar documents"""
        try:
            collection = self.get_or_create_collection(collection_name)
            
            # Convert numpy array to list if needed
            if isinstance(query_embedding, np.ndarray):
                query_embedding = query_embedding.tolist()
            
            # Prepare query parameters
            query_params = {
                "query_embeddings": [query_embedding],
                "n_results": n_results
            }
            
            if filter_criteria:
                query_params["where"] = filter_criteria
            
            results = collection.query(**query_params)
            
            # Format results
            formatted_results = []
            if results['ids'] and results['ids'][0]:
                for i in range(len(results['ids'][0])):
                    formatted_results.append({
                        'id': results['ids'][0][i],
                        'document': results['documents'][0][i] if results['documents'] else None,
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'distance': results['distances'][0][i] if results.get('distances') else None
                    })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            raise VectorStoreException(f"Failed to search: {str(e)}")
    
    async def get_document(self, collection_name: str, doc_id: str) -> Optional[Dict]:
        """Get document by ID"""
        try:
            collection = self.get_or_create_collection(collection_name)
            
            result = collection.get(ids=[doc_id])
            
            if result['ids']:
                return {
                    'id': result['ids'][0],
                    'document': result['documents'][0] if result['documents'] else None,
                    'metadata': result['metadatas'][0] if result['metadatas'] else {}
                }
            return None
            
        except Exception as e:
            logger.error(f"Get document error: {str(e)}")
            raise VectorStoreException(f"Failed to get document: {str(e)}")
    
    async def update_document(
        self,
        collection_name: str,
        doc_id: str,
        document: Optional[str] = None,
        embedding: Optional[List[float]] = None,
        metadata: Optional[Dict] = None
    ):
        """Update document"""
        try:
            collection = self.get_or_create_collection(collection_name)
            
            update_params = {"ids": [doc_id]}
            
            if document:
                update_params["documents"] = [document]
            if embedding:
                if isinstance(embedding, np.ndarray):
                    embedding = embedding.tolist()
                update_params["embeddings"] = [embedding]
            if metadata:
                update_params["metadatas"] = [metadata]
            
            collection.update(**update_params)
            logger.info(f"Updated document {doc_id} in {collection_name}")
            
        except Exception as e:
            logger.error(f"Update error: {str(e)}")
            raise VectorStoreException(f"Failed to update document: {str(e)}")
    
    async def delete_document(self, collection_name: str, doc_id: str):
        """Delete document"""
        try:
            collection = self.get_or_create_collection(collection_name)
            collection.delete(ids=[doc_id])
            logger.info(f"Deleted document {doc_id} from {collection_name}")
            
        except Exception as e:
            logger.error(f"Delete error: {str(e)}")
            raise VectorStoreException(f"Failed to delete document: {str(e)}")
    
    async def list_collections(self) -> List[str]:
        """List all collections"""
        try:
            return self.client.list_collections()
        except Exception as e:
            logger.error(f"List collections error: {str(e)}")
            raise VectorStoreException(f"Failed to list collections: {str(e)}")
    
    async def delete_collection(self, collection_name: str):
        """Delete entire collection"""
        try:
            self.client.delete_collection(collection_name)
            if collection_name in self.collections:
                del self.collections[collection_name]
            logger.info(f"Deleted collection {collection_name}")
            
        except Exception as e:
            logger.error(f"Delete collection error: {str(e)}")
            raise VectorStoreException(f"Failed to delete collection: {str(e)}")
    
    async def count_documents(self, collection_name: str) -> int:
        """Count documents in collection"""
        try:
            collection = self.get_or_create_collection(collection_name)
            return collection.count()
        except Exception as e:
            logger.error(f"Count error: {str(e)}")
            raise VectorStoreException(f"Failed to count documents: {str(e)}")