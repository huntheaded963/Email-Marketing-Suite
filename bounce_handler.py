"""
Bounce Handling Module
معالجة البريد المرتد
"""

from database import get_db, Bounce, Contact, CampaignRecipient
from typing import Dict, List
from datetime import datetime

class BounceHandler:
    """Handle email bounces"""
    
    def record_bounce(self, email: str, bounce_type: str, bounce_reason: str = None,
                     campaign_id: int = None, contact_id: int = None) -> Dict:
        """Record a bounce"""
        db = get_db()
        try:
            # Get contact_id if not provided
            if not contact_id:
                contact = db.query(Contact).filter(Contact.email == email).first()
                if contact:
                    contact_id = contact.id
            
            bounce = Bounce(
                email=email,
                campaign_id=campaign_id,
                contact_id=contact_id,
                bounce_type=bounce_type,  # 'hard' or 'soft'
                bounce_reason=bounce_reason,
                bounced_at=datetime.utcnow()
            )
            db.add(bounce)
            
            # Update contact status if hard bounce
            if bounce_type == 'hard' and contact_id:
                contact = db.query(Contact).filter(Contact.id == contact_id).first()
                if contact:
                    contact.status = 'bounced'
            
            # Update campaign recipient status
            if campaign_id and contact_id:
                recipient = db.query(CampaignRecipient).filter(
                    CampaignRecipient.campaign_id == campaign_id,
                    CampaignRecipient.contact_id == contact_id
                ).first()
                if recipient:
                    recipient.status = 'bounced'
            
            db.commit()
            return {'status': 'success', 'bounce': bounce}
        except Exception as e:
            db.rollback()
            return {'status': 'error', 'message': str(e)}
        finally:
            db.close()
    
    def get_bounces(self, email: str = None, campaign_id: int = None, 
                   bounce_type: str = None, limit: int = 100) -> List[Bounce]:
        """Get bounce records"""
        db = get_db()
        try:
            query = db.query(Bounce)
            
            if email:
                query = query.filter(Bounce.email == email)
            if campaign_id:
                query = query.filter(Bounce.campaign_id == campaign_id)
            if bounce_type:
                query = query.filter(Bounce.bounce_type == bounce_type)
            
            return query.order_by(Bounce.bounced_at.desc()).limit(limit).all()
        finally:
            db.close()
    
    def get_bounce_stats(self) -> Dict:
        """Get bounce statistics"""
        db = get_db()
        try:
            total_bounces = db.query(Bounce).count()
            hard_bounces = db.query(Bounce).filter(Bounce.bounce_type == 'hard').count()
            soft_bounces = db.query(Bounce).filter(Bounce.bounce_type == 'soft').count()
            
            # Get unique bounced emails
            unique_bounced = db.query(Bounce.email).distinct().count()
            
            return {
                'total_bounces': total_bounces,
                'hard_bounces': hard_bounces,
                'soft_bounces': soft_bounces,
                'unique_bounced_emails': unique_bounced,
                'bounce_rate': 0  # Will be calculated based on sent emails
            }
        finally:
            db.close()
    
    def is_bounced(self, email: str) -> bool:
        """Check if email has hard bounced"""
        db = get_db()
        try:
            hard_bounce = db.query(Bounce).filter(
                Bounce.email == email,
                Bounce.bounce_type == 'hard'
            ).first()
            return hard_bounce is not None
        finally:
            db.close()

