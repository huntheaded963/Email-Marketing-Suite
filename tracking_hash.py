"""
Tracking hash generator for email open tracking
"""
import hashlib
import secrets
from typing import Optional
from datetime import datetime
from database import get_db, Contact, CampaignRecipient, EmailOpen

class TrackingHashGenerator:
    """Generate and manage tracking hashes for emails"""
    
    @staticmethod
    def generate_hash(email: str, campaign_id: int, contact_id: int) -> str:
        """Generate unique hash for email tracking"""
        # Create a unique string from email, campaign, and contact
        unique_string = f"{email}_{campaign_id}_{contact_id}_{secrets.token_hex(8)}"
        # Generate hash
        hash_value = hashlib.sha256(unique_string.encode()).hexdigest()
        return hash_value
    
    @staticmethod
    def get_or_create_hash(email: str, campaign_id: int, contact_id: int) -> str:
        """Get existing hash or create new one"""
        db = get_db()
        try:
            # Check if hash already exists for this email/campaign combination
            existing = db.query(EmailOpen).filter(
                EmailOpen.email == email,
                EmailOpen.campaign_id == campaign_id,
                EmailOpen.contact_id == contact_id
            ).first()
            
            if existing:
                return existing.hash_value
            
            # Create new hash
            hash_value = TrackingHashGenerator.generate_hash(email, campaign_id, contact_id)
            
            # Store in database
            email_open = EmailOpen(
                email=email,
                campaign_id=campaign_id,
                contact_id=contact_id,
                hash_value=hash_value,
                open_count=0  # Will be incremented when opened
            )
            db.add(email_open)
            db.commit()
            
            return hash_value
        except Exception as e:
            db.rollback()
            # If error, generate hash anyway (for sending)
            return TrackingHashGenerator.generate_hash(email, campaign_id, contact_id)
        finally:
            db.close()
    
    @staticmethod
    def get_hash_by_value(hash_value: str) -> Optional[EmailOpen]:
        """Get email open record by hash"""
        db = get_db()
        try:
            return db.query(EmailOpen).filter(EmailOpen.hash_value == hash_value).first()
        finally:
            db.close()
    
    @staticmethod
    def record_open(hash_value: str, ip_address: str = None, user_agent: str = None, country: str = None) -> dict:
        """Record email open event"""
        db = get_db()
        try:
            email_open = db.query(EmailOpen).filter(EmailOpen.hash_value == hash_value).first()
            
            if email_open:
                # Update open count and timestamp
                email_open.open_count += 1
                if not email_open.opened_at:
                    email_open.opened_at = datetime.utcnow()
                if ip_address:
                    email_open.ip_address = ip_address
                if user_agent:
                    email_open.user_agent = user_agent
                if country:
                    email_open.country = country
                
                # Update campaign recipient status
                recipient = db.query(CampaignRecipient).filter(
                    CampaignRecipient.campaign_id == email_open.campaign_id,
                    CampaignRecipient.contact_id == email_open.contact_id
                ).first()
                
                if recipient:
                    recipient.status = 'opened'
                    recipient.open_count = email_open.open_count
                    if not recipient.opened_at:
                        recipient.opened_at = datetime.utcnow()
                
                db.commit()
                return {'status': 'success', 'email_open': email_open}
            else:
                return {'status': 'not_found', 'message': 'Hash not found'}
        except Exception as e:
            db.rollback()
            return {'status': 'error', 'message': str(e)}
        finally:
            db.close()

