"""Music discovery and cataloging system."""

import os
import sqlite3
import hashlib
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging

import mutagen
from mutagen.id3 import ID3NoHeaderError
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
from mutagen.oggvorbis import OggVorbis

logger = logging.getLogger(__name__)

@dataclass
class Track:
    """Represents a music track."""
    file_path: str
    title: str
    artist: str
    album: str
    genre: str
    year: Optional[int]
    duration: float
    file_size: int
    file_hash: str
    last_modified: datetime
    bitrate: Optional[int] = None
    sample_rate: Optional[int] = None

class MusicDiscovery:
    """Discovers and catalogs music files from local directories."""
    
    SUPPORTED_FORMATS = {'.mp3', '.flac', '.m4a', '.ogg', '.wav', '.aac'}
    
    def __init__(self, db_path: str):
        """Initialize music discovery with database path."""
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize the music database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tracks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT UNIQUE NOT NULL,
                    title TEXT,
                    artist TEXT,
                    album TEXT,
                    genre TEXT,
                    year INTEGER,
                    duration REAL,
                    file_size INTEGER,
                    file_hash TEXT,
                    last_modified TIMESTAMP,
                    bitrate INTEGER,
                    sample_rate INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_artist ON tracks(artist)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_genre ON tracks(genre)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_year ON tracks(year)
            """)
    
    def _get_file_hash(self, file_path: str) -> str:
        """Generate hash for file to detect changes."""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def _extract_metadata(self, file_path: str) -> Dict:
        """Extract metadata from audio file."""
        try:
            audio_file = mutagen.File(file_path)
            if audio_file is None:
                return {}
            
            metadata = {}
            
            # Common tags across formats
            if hasattr(audio_file, 'tags') and audio_file.tags:
                tags = audio_file.tags
                
                # Title
                if 'TIT2' in tags:  # ID3v2
                    metadata['title'] = str(tags['TIT2'][0])
                elif 'TITLE' in tags:  # Vorbis/FLAC
                    metadata['title'] = str(tags['TITLE'][0])
                elif '\xa9nam' in tags:  # MP4
                    metadata['title'] = str(tags['\xa9nam'][0])
                
                # Artist
                if 'TPE1' in tags:  # ID3v2
                    metadata['artist'] = str(tags['TPE1'][0])
                elif 'ARTIST' in tags:  # Vorbis/FLAC
                    metadata['artist'] = str(tags['ARTIST'][0])
                elif '\xa9ART' in tags:  # MP4
                    metadata['artist'] = str(tags['\xa9ART'][0])
                
                # Album
                if 'TALB' in tags:  # ID3v2
                    metadata['album'] = str(tags['TALB'][0])
                elif 'ALBUM' in tags:  # Vorbis/FLAC
                    metadata['album'] = str(tags['ALBUM'][0])
                elif '\xa9alb' in tags:  # MP4
                    metadata['album'] = str(tags['\xa9alb'][0])
                
                # Genre
                if 'TCON' in tags:  # ID3v2
                    metadata['genre'] = str(tags['TCON'][0])
                elif 'GENRE' in tags:  # Vorbis/FLAC
                    metadata['genre'] = str(tags['GENRE'][0])
                elif '\xa9gen' in tags:  # MP4
                    metadata['genre'] = str(tags['\xa9gen'][0])
                
                # Year
                if 'TDRC' in tags:  # ID3v2
                    year_str = str(tags['TDRC'][0])
                    if year_str.isdigit():
                        metadata['year'] = int(year_str)
                elif 'DATE' in tags:  # Vorbis/FLAC
                    year_str = str(tags['DATE'][0])
                    if year_str.isdigit():
                        metadata['year'] = int(year_str)
                elif '\xa9day' in tags:  # MP4
                    year_str = str(tags['\xa9day'][0])
                    if year_str.isdigit():
                        metadata['year'] = int(year_str)
            
            # Audio properties
            if hasattr(audio_file, 'info'):
                info = audio_file.info
                metadata['duration'] = getattr(info, 'length', 0.0)
                metadata['bitrate'] = getattr(info, 'bitrate', None)
                metadata['sample_rate'] = getattr(info, 'sample_rate', None)
            
            return metadata
            
        except Exception as e:
            logger.warning(f"Error extracting metadata from {file_path}: {e}")
            return {}
    
    def _create_track_from_file(self, file_path: str) -> Optional[Track]:
        """Create Track object from file path."""
        try:
            file_path = Path(file_path).resolve()
            stat = file_path.stat()
            
            # Extract metadata
            metadata = self._extract_metadata(str(file_path))
            
            # Generate file hash
            file_hash = self._get_file_hash(str(file_path))
            
            # Create track
            track = Track(
                file_path=str(file_path),
                title=metadata.get('title', file_path.stem),
                artist=metadata.get('artist', 'Unknown Artist'),
                album=metadata.get('album', 'Unknown Album'),
                genre=metadata.get('genre', 'Unknown'),
                year=metadata.get('year'),
                duration=metadata.get('duration', 0.0),
                file_size=stat.st_size,
                file_hash=file_hash,
                last_modified=datetime.fromtimestamp(stat.st_mtime),
                bitrate=metadata.get('bitrate'),
                sample_rate=metadata.get('sample_rate')
            )
            
            return track
            
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            return None
    
    def scan_directory(self, directory: str) -> List[Track]:
        """Scan directory for music files and return list of tracks."""
        tracks = []
        directory = Path(directory)
        
        if not directory.exists():
            logger.warning(f"Directory does not exist: {directory}")
            return tracks
        
        logger.info(f"Scanning directory: {directory}")
        
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_FORMATS:
                track = self._create_track_from_file(str(file_path))
                if track:
                    tracks.append(track)
        
        logger.info(f"Found {len(tracks)} music files in {directory}")
        return tracks
    
    def scan_directories(self, directories: List[str]) -> List[Track]:
        """Scan multiple directories for music files."""
        all_tracks = []
        
        for directory in directories:
            tracks = self.scan_directory(directory)
            all_tracks.extend(tracks)
        
        return all_tracks
    
    def save_tracks(self, tracks: List[Track]) -> int:
        """Save tracks to database, updating existing ones."""
        saved_count = 0
        
        with sqlite3.connect(self.db_path) as conn:
            for track in tracks:
                try:
                    conn.execute("""
                        INSERT OR REPLACE INTO tracks 
                        (file_path, title, artist, album, genre, year, duration, 
                         file_size, file_hash, last_modified, bitrate, sample_rate)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        track.file_path, track.title, track.artist, track.album,
                        track.genre, track.year, track.duration, track.file_size,
                        track.file_hash, track.last_modified, track.bitrate,
                        track.sample_rate
                    ))
                    saved_count += 1
                except Exception as e:
                    logger.error(f"Error saving track {track.file_path}: {e}")
        
        logger.info(f"Saved {saved_count} tracks to database")
        return saved_count
    
    def get_all_tracks(self) -> List[Track]:
        """Get all tracks from database."""
        tracks = []
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM tracks ORDER BY artist, album, title")
            
            for row in cursor:
                track = Track(
                    file_path=row['file_path'],
                    title=row['title'],
                    artist=row['artist'],
                    album=row['album'],
                    genre=row['genre'],
                    year=row['year'],
                    duration=row['duration'],
                    file_size=row['file_size'],
                    file_hash=row['file_hash'],
                    last_modified=datetime.fromisoformat(row['last_modified']),
                    bitrate=row['bitrate'],
                    sample_rate=row['sample_rate']
                )
                tracks.append(track)
        
        return tracks
    
    def search_tracks(self, query: str = "", artist: str = "", genre: str = "", 
                     year: Optional[int] = None) -> List[Track]:
        """Search tracks by various criteria."""
        tracks = []
        conditions = []
        params = []
        
        if query:
            conditions.append("(title LIKE ? OR artist LIKE ? OR album LIKE ?)")
            params.extend([f"%{query}%", f"%{query}%", f"%{query}%"])
        
        if artist:
            conditions.append("artist LIKE ?")
            params.append(f"%{artist}%")
        
        if genre:
            conditions.append("genre LIKE ?")
            params.append(f"%{genre}%")
        
        if year:
            conditions.append("year = ?")
            params.append(year)
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                f"SELECT * FROM tracks WHERE {where_clause} ORDER BY artist, album, title",
                params
            )
            
            for row in cursor:
                track = Track(
                    file_path=row['file_path'],
                    title=row['title'],
                    artist=row['artist'],
                    album=row['album'],
                    genre=row['genre'],
                    year=row['year'],
                    duration=row['duration'],
                    file_size=row['file_size'],
                    file_hash=row['file_hash'],
                    last_modified=datetime.fromisoformat(row['last_modified']),
                    bitrate=row['bitrate'],
                    sample_rate=row['sample_rate']
                )
                tracks.append(track)
        
        return tracks
    
    def get_stats(self) -> Dict:
        """Get statistics about the music library."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT 
                    COUNT(*) as total_tracks,
                    COUNT(DISTINCT artist) as unique_artists,
                    COUNT(DISTINCT album) as unique_albums,
                    COUNT(DISTINCT genre) as unique_genres,
                    SUM(duration) as total_duration,
                    SUM(file_size) as total_size
                FROM tracks
            """)
            
            row = cursor.fetchone()
            return dict(row)
