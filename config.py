"""
Configuration module for Email Marketing Application
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///email_marketing.db')
    
    # SMTP Settings (default - user should configure)
    SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USER = os.getenv('SMTP_USER', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    SMTP_USE_TLS = os.getenv('SMTP_USE_TLS', 'True').lower() == 'true'
    
    # Application Settings
    MAX_EMAILS_PER_BATCH = int(os.getenv('MAX_EMAILS_PER_BATCH', '50'))
    DELAY_BETWEEN_EMAILS = float(os.getenv('DELAY_BETWEEN_EMAILS', '1.0'))
    
    # Tracking
    TRACK_OPENS = os.getenv('TRACK_OPENS', 'True').lower() == 'true'
    TRACK_CLICKS = os.getenv('TRACK_CLICKS', 'True').lower() == 'true'

