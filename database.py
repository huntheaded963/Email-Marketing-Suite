"""
Database Connection Manager
Handles SQLite database connections and initialization
"""

import sqlite3
from pathlib import Path
from typing import Optional
from contextlib import contextmanager
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(50))
    company = Column(String(200))
    tags = Column(Text)
    status = Column(String(20), default='active')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class ContactList(Base):
    __tablename__ = 'contact_lists'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    members = relationship('ContactListMember', back_populates='contact_list')

class ContactListMember(Base):
    __tablename__ = 'contact_list_members'
    id = Column(Integer, primary_key=True)
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    contact_list_id = Column(Integer, ForeignKey('contact_lists.id'))
    added_at = Column(DateTime, default=datetime.now)
    contact = relationship('Contact', back_populates='list_members')
    contact_list = relationship('ContactList', back_populates='members')

Contact.list_members = relationship('ContactListMember', back_populates='contact')

class Campaign(Base):
    __tablename__ = 'campaigns'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    subject = Column(String(500))
    body_html = Column(Text)
    body_text = Column(Text)
    template_id = Column(Integer)
    status = Column(String(20), default='draft')
    scheduled_at = Column(DateTime)
    sent_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    recipients = relationship('CampaignRecipient', back_populates='campaign')

class CampaignRecipient(Base):
    __tablename__ = 'campaign_recipients'
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    email = Column(String(255))
    status = Column(String(20), default='pending')
    sent_at = Column(DateTime)
    opened_at = Column(DateTime)
    clicked_at = Column(DateTime)
    bounced_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    campaign = relationship('Campaign', back_populates='recipients')
    contact = relationship('Contact')

Campaign.recipients = relationship('CampaignRecipient', back_populates='campaign')

class Segment(Base):
    __tablename__ = 'segments'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    criteria = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    members = relationship('SegmentMember', back_populates='segment')

class SegmentMember(Base):
    __tablename__ = 'segment_members'
    id = Column(Integer, primary_key=True)
    segment_id = Column(Integer, ForeignKey('segments.id'))
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    added_at = Column(DateTime, default=datetime.now)
    segment = relationship('Segment', back_populates='members')
    contact = relationship('Contact')

class Bounce(Base):
    __tablename__ = 'bounces'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    bounce_type = Column(String(50))
    bounce_message = Column(Text)
    bounced_at = Column(DateTime, default=datetime.now)
    campaign = relationship('Campaign')

class Unsubscribe(Base):
    __tablename__ = 'unsubscribes'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    unsubscribed_at = Column(DateTime, default=datetime.now)
    campaign = relationship('Campaign')

class EmailTemplate(Base):
    __tablename__ = 'email_templates'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    subject = Column(String(500))
    body_html = Column(Text)
    body_text = Column(Text)
    category = Column(String(50))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class EmailOpenRecord(Base):
    __tablename__ = 'email_opens'
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    email_address = Column(String(255))
    opened_at = Column(DateTime, default=datetime.now)
    user_agent = Column(Text)
    ip_address = Column(String(50))
    campaign = relationship('Campaign')
    contact = relationship('Contact')

EmailOpen = EmailOpenRecord

engine = create_engine('sqlite:///email_marketing.db', echo=False)

_engine = None
_Session = None

def get_db():
    """Get SQLAlchemy session"""
    global _engine, _Session
    if _engine is None:
        _engine = create_engine('sqlite:///email_marketing.db', echo=False)
        Base.metadata.create_all(_engine)
    if _Session is None:
        _Session = sessionmaker(bind=_engine)
    return _Session()


class DatabaseManager:
    """Manages database connections and schema initialization"""
    
    def __init__(self, db_path: str = "erp_app.db"):
        """
        Initialize database manager
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self._ensure_database()
    
    def _ensure_database(self):
        """Ensure database file exists and schema is initialized"""
        if not self.db_path.exists():
            # Create database file
            self.db_path.touch()
            # Initialize schema
            self._initialize_schema()
        else:
            # Check if schema exists, if not initialize
            self._initialize_schema()
    
    def _initialize_schema(self):
        """Initialize database schema from SQL file"""
        schema_file = Path(__file__).parent.parent / "storage" / "erp_schema.sql"
        
        if schema_file.exists():
            with self.get_connection() as conn:
                with open(schema_file, 'r', encoding='utf-8') as f:
                    schema_sql = f.read()
                    conn.executescript(schema_sql)
                    conn.commit()
    
    @contextmanager
    def get_connection(self):
        """
        Get database connection (context manager)
        
        Usage:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM ...")
        """
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row  # Return rows as dict-like objects
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign keys
        
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def get_connection_sync(self) -> sqlite3.Connection:
        """
        Get database connection (synchronous, manual management)
        
        Returns:
            sqlite3.Connection: Database connection
            
        Note: You must manually close this connection
        """
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    
    def execute_script(self, script_path: Path):
        """Execute SQL script file"""
        with self.get_connection() as conn:
            with open(script_path, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
                conn.commit()
    
    def backup(self, backup_path: Optional[Path] = None):
        """
        Create database backup
        
        Args:
            backup_path: Path for backup file (default: db_path.backup)
        """
        if backup_path is None:
            backup_path = self.db_path.with_suffix('.backup.db')
        
        import shutil
        shutil.copy2(self.db_path, backup_path)
        return backup_path
    
    def restore(self, backup_path: Path):
        """
        Restore database from backup
        
        Args:
            backup_path: Path to backup file
        """
        import shutil
        shutil.copy2(backup_path, self.db_path)


# Global database manager instance
_db_manager: Optional[DatabaseManager] = None


def get_db_manager(db_path: str = "erp_app.db") -> DatabaseManager:
    """
    Get global database manager instance
    
    Args:
        db_path: Path to database file
        
    Returns:
        DatabaseManager: Database manager instance
    """
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager(db_path)
    return _db_manager


def get_connection():
    """
    Get database connection (convenience function)
    
    Returns:
        Context manager for database connection
    """
    return get_db_manager().get_connection()


class EmailOpen:
    """Email tracking model"""
    def __init__(self, id=None, campaign_id=None, contact_id=None, 
                 email_address=None, timestamp=None, user_agent=None, ip_address=None):
        self.id = id
        self.campaign_id = campaign_id
        self.contact_id = contact_id
        self.email_address = email_address
        self.timestamp = timestamp or datetime.now()
        self.user_agent = user_agent
        self.ip_address = ip_address


def init_db():
    """Initialize database with schema for email marketing"""
    db = get_db_manager()
    with db.get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                first_name TEXT,
                last_name TEXT,
                phone TEXT,
                company TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                subject TEXT,
                body TEXT,
                status TEXT DEFAULT 'draft',
                scheduled_at TIMESTAMP,
                sent_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS email_opens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id INTEGER,
                contact_id INTEGER,
                email_address TEXT,
                opened_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_agent TEXT,
                ip_address TEXT,
                FOREIGN KEY (campaign_id) REFERENCES campaigns(id),
                FOREIGN KEY (contact_id) REFERENCES contacts(id)
            );
            
            CREATE TABLE IF NOT EXISTS email_clicks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id INTEGER,
                contact_id INTEGER,
                email_address TEXT,
                url TEXT,
                clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (campaign_id) REFERENCES campaigns(id),
                FOREIGN KEY (contact_id) REFERENCES contacts(id)
            );
            
            CREATE TABLE IF NOT EXISTS bounces (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                campaign_id INTEGER,
                bounce_type TEXT,
                bounce_message TEXT,
                bounced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
            );
            
            CREATE TABLE IF NOT EXISTS unsubscribes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                campaign_id INTEGER,
                unsubscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
            );
        """)
    print("Database initialized successfully!")


# Initialize database on import
init_db()
