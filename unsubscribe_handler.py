"""
Unsubscribe Management Module
إدارة إلغاء الاشتراك
"""

from database import get_db, Unsubscribe, Contact, CampaignRecipient
from typing import Dict, List
from datetime import datetime
import hashlib

class UnsubscribeHandler:
    """Handle unsubscribes"""
    
    def generate_unsubscribe_hash(self, email: str) -> str:
        """Generate hash for unsubscribe link"""
        secret = "unsubscribe_secret_key"  # Should be in config
        hash_string = f"{email}_{secret}"
        return hashlib.sha256(hash_string.encode()).hexdigest()
    
    def unsubscribe(self, email: str, reason: str = None, ip_address: str = None, 
                   hash_value: str = None) -> Dict:
        """Unsubscribe an email"""
        db = get_db()
        try:
            # Verify hash if provided
            if hash_value:
                expected_hash = self.generate_unsubscribe_hash(email)
                if hash_value != expected_hash:
                    return {'status': 'error', 'message': 'Invalid hash'}
            
            # Check if already unsubscribed
            existing = db.query(Unsubscribe).filter(Unsubscribe.email == email).first()
            if existing:
                return {'status': 'exists', 'message': 'Already unsubscribed'}
            
            # Get contact_id
            contact = db.query(Contact).filter(Contact.email == email).first()
            contact_id = contact.id if contact else None
            
            # Create unsubscribe record
            unsubscribe = Unsubscribe(
                email=email,
                contact_id=contact_id,
                reason=reason,
                unsubscribed_at=datetime.utcnow(),
                ip_address=ip_address
            )
            db.add(unsubscribe)
            
            # Update contact status
            if contact:
                contact.status = 'unsubscribed'
            
            # Update all campaign recipients for this contact
            if contact_id:
                recipients = db.query(CampaignRecipient).filter(
                    CampaignRecipient.contact_id == contact_id
                ).all()
                for recipient in recipients:
                    if recipient.status == 'pending':
                        recipient.status = 'unsubscribed'
            
            db.commit()
            return {'status': 'success', 'unsubscribe': unsubscribe}
        except Exception as e:
            db.rollback()
            return {'status': 'error', 'message': str(e)}
        finally:
            db.close()
    
    def is_unsubscribed(self, email: str) -> bool:
        """Check if email is unsubscribed"""
        db = get_db()
        try:
            unsubscribe = db.query(Unsubscribe).filter(Unsubscribe.email == email).first()
            return unsubscribe is not None
        finally:
            db.close()
    
    def get_unsubscribes(self, limit: int = 100) -> List[Unsubscribe]:
        """Get list of unsubscribes"""
        db = get_db()
        try:
            return db.query(Unsubscribe).order_by(Unsubscribe.unsubscribed_at.desc()).limit(limit).all()
        finally:
            db.close()
    
    def get_unsubscribe_stats(self) -> Dict:
        """Get unsubscribe statistics"""
        db = get_db()
        try:
            total_unsubscribes = db.query(Unsubscribe).count()
            
            # Get unsubscribes by reason (if tracked)
            return {
                'total_unsubscribes': total_unsubscribes,
                'unsubscribe_rate': 0  # Will be calculated based on sent emails
            }
        finally:
            db.close()
    
    def resubscribe(self, email: str) -> Dict:
        """Resubscribe an email"""
        db = get_db()
        try:
            unsubscribe = db.query(Unsubscribe).filter(Unsubscribe.email == email).first()
            if not unsubscribe:
                return {'status': 'not_found', 'message': 'Email not in unsubscribe list'}
            
            # Remove from unsubscribe list
            db.delete(unsubscribe)
            
            # Update contact status
            contact = db.query(Contact).filter(Contact.email == email).first()
            if contact:
                contact.status = 'active'
            
            db.commit()
            return {'status': 'success', 'message': 'Email resubscribed'}
        except Exception as e:
            db.rollback()
            return {'status': 'error', 'message': str(e)}
        finally:
            db.close()

