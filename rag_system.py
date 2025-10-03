"""RAG (Retrieval-Augmented Generation) system for personalized radio content."""

import os
import json
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import requests

# RAG dependencies
try:
    import chromadb
    from sentence_transformers import SentenceTransformer
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.schema import Document
except ImportError:
    chromadb = None
    SentenceTransformer = None
    RecursiveCharacterTextSplitter = None
    Document = None
    logging.warning("RAG dependencies not available. Install with: pip install chromadb sentence-transformers langchain")

logger = logging.getLogger(__name__)

@dataclass
class PersonalContext:
    """Personal context information for radio personalization."""
    name: str
    location: str
    interests: List[str]
    music_preferences: List[str]
    time_preferences: Dict[str, Any]
    weather_preferences: Dict[str, Any]
    personal_events: List[Dict[str, Any]]
    listening_history: List[Dict[str, Any]]

class WeatherService:
    """Weather service for real-time weather data."""
    
    def __init__(self, api_key: str, city: str, country: str = "GB"):
        """Initialize weather service."""
        self.api_key = api_key
        self.city = city
        self.country = country
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.last_update = None
        self.cached_data = None
    
    async def get_current_weather(self) -> Optional[Dict]:
        """Get current weather data."""
        # Cache for 10 minutes
        if (self.last_update and 
            datetime.now() - self.last_update < timedelta(minutes=10) and 
            self.cached_data):
            return self.cached_data
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                "q": f"{self.city},{self.country}",
                "appid": self.api_key,
                "units": "metric"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            weather_data = {
                "temperature": round(data["main"]["temp"]),
                "feels_like": round(data["main"]["feels_like"]),
                "humidity": data["main"]["humidity"],
                "condition": data["weather"][0]["description"],
                "wind_speed": data["wind"]["speed"],
                "city": self.city,
                "country": self.country,
                "timestamp": datetime.now().isoformat()
            }
            
            self.cached_data = weather_data
            self.last_update = datetime.now()
            
            return weather_data
            
        except Exception as e:
            logger.error(f"Failed to get weather data: {e}")
            return None

class RAGSystem:
    """RAG system for personalized radio content generation."""
    
    def __init__(self, collection_name: str = "personal_radio_context", 
                 embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
                 db_path: str = "data/rag.db"):
        """Initialize RAG system."""
        self.collection_name = collection_name
        self.embedding_model_name = embedding_model
        self.db_path = db_path
        
        # Initialize components
        self.client = None
        self.collection = None
        self.embedding_model = None
        self.text_splitter = None
        self.weather_service = None
        
        # Personal context
        self.personal_context = None
        
        # Initialize system
        self._initialize_system()
    
    def _initialize_system(self):
        """Initialize RAG system components."""
        if not all([chromadb, SentenceTransformer, RecursiveCharacterTextSplitter]):
            logger.warning("RAG dependencies not available. RAG features will be limited.")
            return
        
        try:
            # Initialize ChromaDB
            self.client = chromadb.PersistentClient(path=self.db_path)
            
            # Get or create collection
            try:
                self.collection = self.client.get_collection(self.collection_name)
            except ValueError:
                self.collection = self.client.create_collection(
                    name=self.collection_name,
                    metadata={"description": "Personal radio context and preferences"}
                )
            
            # Initialize embedding model
            self.embedding_model = SentenceTransformer(self.embedding_model_name)
            
            # Initialize text splitter
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            
            logger.info("RAG system initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG system: {e}")
    
    def set_weather_service(self, api_key: str, city: str, country: str = "GB"):
        """Set up weather service."""
        self.weather_service = WeatherService(api_key, city, country)
    
    def set_personal_context(self, context: PersonalContext):
        """Set personal context for personalization."""
        self.personal_context = context
        self._update_context_in_db()
    
    def _update_context_in_db(self):
        """Update personal context in database."""
        if not self.collection or not self.personal_context:
            return
        
        try:
            # Create context documents
            context_text = f"""
            Personal Information:
            Name: {self.personal_context.name}
            Location: {self.personal_context.location}
            Interests: {', '.join(self.personal_context.interests)}
            Music Preferences: {', '.join(self.personal_context.music_preferences)}
            Time Preferences: {json.dumps(self.personal_context.time_preferences)}
            Weather Preferences: {json.dumps(self.personal_context.weather_preferences)}
            """
            
            # Split into chunks
            documents = self.text_splitter.split_text(context_text)
            
            # Add to collection
            for i, doc in enumerate(documents):
                self.collection.add(
                    documents=[doc],
                    metadatas=[{"type": "personal_context", "chunk": i}],
                    ids=[f"personal_context_{i}"]
                )
            
            logger.info("Personal context updated in database")
            
        except Exception as e:
            logger.error(f"Failed to update personal context: {e}")
    
    def add_document(self, content: str, metadata: Dict = None, doc_id: str = None):
        """Add document to RAG system."""
        if not self.collection:
            return False
        
        try:
            # Split document into chunks
            documents = self.text_splitter.split_text(content)
            
            # Prepare metadata
            if metadata is None:
                metadata = {}
            
            # Add each chunk
            for i, doc in enumerate(documents):
                chunk_id = f"{doc_id}_{i}" if doc_id else f"doc_{datetime.now().timestamp()}_{i}"
                chunk_metadata = metadata.copy()
                chunk_metadata["chunk"] = i
                
                self.collection.add(
                    documents=[doc],
                    metadatas=[chunk_metadata],
                    ids=[chunk_id]
                )
            
            logger.info(f"Added document with {len(documents)} chunks")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add document: {e}")
            return False
    
    def query_context(self, query: str, n_results: int = 5) -> List[Dict]:
        """Query context for relevant information."""
        if not self.collection:
            return []
        
        try:
            # Query collection
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            # Format results
            formatted_results = []
            for i, (doc, metadata, distance) in enumerate(zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            )):
                formatted_results.append({
                    "content": doc,
                    "metadata": metadata,
                    "similarity": 1 - distance,  # Convert distance to similarity
                    "rank": i + 1
                })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Failed to query context: {e}")
            return []
    
    async def get_weather_context(self) -> Optional[Dict]:
        """Get current weather context."""
        if not self.weather_service:
            return None
        
        return await self.weather_service.get_current_weather()
    
    def generate_personalized_content(self, base_content: str, context_type: str = "general") -> str:
        """Generate personalized content based on context."""
        if not self.personal_context:
            return base_content
        
        # Query relevant context
        context_results = self.query_context(base_content, n_results=3)
        
        # Build personalized content
        personalized_content = base_content
        
        # Add personal touches based on context
        if context_type == "music_intro":
            if self.personal_context.music_preferences:
                genre_pref = self.personal_context.music_preferences[0]
                personalized_content += f" I know you enjoy {genre_pref} music."
        
        elif context_type == "weather":
            if self.personal_context.weather_preferences:
                weather_pref = self.personal_context.weather_preferences.get("preferred_conditions", "")
                if weather_pref:
                    personalized_content += f" Perfect weather for {weather_pref}!"
        
        elif context_type == "time_announcement":
            current_hour = datetime.now().hour
            if 6 <= current_hour < 12:
                personalized_content += " Good morning!"
            elif 12 <= current_hour < 17:
                personalized_content += " Good afternoon!"
            elif 17 <= current_hour < 21:
                personalized_content += " Good evening!"
            else:
                personalized_content += " Good night!"
        
        return personalized_content
    
    def get_recommendations(self, query: str, context_type: str = "music") -> List[str]:
        """Get personalized recommendations."""
        if not self.personal_context:
            return []
        
        # Query relevant context
        context_results = self.query_context(query, n_results=5)
        
        recommendations = []
        
        if context_type == "music":
            # Music recommendations based on preferences
            for pref in self.personal_context.music_preferences:
                if pref.lower() in query.lower():
                    recommendations.append(f"More {pref} music coming up")
        
        elif context_type == "content":
            # Content recommendations based on interests
            for interest in self.personal_context.interests:
                if interest.lower() in query.lower():
                    recommendations.append(f"Let's talk about {interest}")
        
        return recommendations
    
    def add_listening_event(self, track_title: str, artist: str, duration: float):
        """Add listening event to history."""
        if not self.personal_context:
            return
        
        event = {
            "track_title": track_title,
            "artist": artist,
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        }
        
        self.personal_context.listening_history.append(event)
        
        # Keep only last 100 events
        if len(self.personal_context.listening_history) > 100:
            self.personal_context.listening_history = self.personal_context.listening_history[-100:]
    
    def get_listening_stats(self) -> Dict:
        """Get listening statistics."""
        if not self.personal_context or not self.personal_context.listening_history:
            return {}
        
        history = self.personal_context.listening_history
        
        # Calculate stats
        total_tracks = len(history)
        total_duration = sum(event["duration"] for event in history)
        
        # Most played artists
        artist_counts = {}
        for event in history:
            artist = event["artist"]
            artist_counts[artist] = artist_counts.get(artist, 0) + 1
        
        top_artists = sorted(artist_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "total_tracks": total_tracks,
            "total_duration_hours": round(total_duration / 3600, 2),
            "top_artists": top_artists,
            "recent_tracks": history[-10:] if history else []
        }
    
    def is_available(self) -> bool:
        """Check if RAG system is available."""
        return (self.client is not None and 
                self.collection is not None and 
                self.embedding_model is not None)
    
    def get_system_info(self) -> Dict:
        """Get RAG system information."""
        return {
            "available": self.is_available(),
            "collection_name": self.collection_name,
            "embedding_model": self.embedding_model_name,
            "personal_context_loaded": self.personal_context is not None,
            "weather_service_available": self.weather_service is not None
        }
