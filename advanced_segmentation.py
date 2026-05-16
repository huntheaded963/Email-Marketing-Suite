"""
Advanced Segmentation Engine
محرك التقسيم المتقدم
"""

from database import get_db, Contact, EmailOpen, CampaignRecipient, Segment
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from sqlalchemy import func, and_, or_

class AdvancedSegmentation:
    """Advanced segmentation based on behavior, demographics, and lifecycle"""
    
    def segment_by_behavior(self, behavior_type: str, days: int = 30, 
                            threshold: int = 1) -> List[Contact]:
        """Segment contacts by behavior"""
        db = get_db()
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            if behavior_type == 'high_engagement':
                # Contacts who opened/clicked frequently
                contacts = db.query(Contact).join(
                    EmailOpen, Contact.id == EmailOpen.contact_id
                ).filter(
                    EmailOpen.opened_at >= cutoff_date
                ).group_by(Contact.id).having(
                    func.count(EmailOpen.id) >= threshold
                ).all()
            
            elif behavior_type == 'low_engagement':
                # Contacts with no opens in period
                contacts = db.query(Contact).filter(
                    ~Contact.id.in_(
                        db.query(EmailOpen.contact_id).filter(
                            EmailOpen.opened_at >= cutoff_date
                        )
                    )
                ).all()
            
            elif behavior_type == 'clickers':
                # Contacts who clicked links
                contacts = db.query(Contact).join(
                    CampaignRecipient, Contact.id == CampaignRecipient.contact_id
                ).filter(
                    CampaignRecipient.click_count > 0,
                    CampaignRecipient.clicked_at >= cutoff_date
                ).distinct().all()
            
            elif behavior_type == 'recent_subscribers':
                # New subscribers
                contacts = db.query(Contact).filter(
                    Contact.created_at >= cutoff_date
                ).all()
            
            else:
                contacts = []
            
            return contacts
        finally:
            db.close()
    
    def segment_by_demographics(self, field: str, value: str) -> List[Contact]:
        """Segment by demographic data"""
        db = get_db()
        try:
            if field == 'location' or field == 'country':
                # Would need location field in Contact model
                contacts = db.query(Contact).filter(
                    Contact.tags.contains(value)
                ).all()
            elif field == 'status':
                contacts = db.query(Contact).filter(Contact.status == value).all()
            else:
                contacts = []
            
            return contacts
        finally:
            db.close()
    
    def segment_by_lifecycle(self, stage: str) -> List[Contact]:
        """Segment by lifecycle stage"""
        db = get_db()
        try:
            now = datetime.utcnow()
            thirty_days_ago = now - timedelta(days=30)
            ninety_days_ago = now - timedelta(days=90)
            
            if stage == 'new':
                # Subscribed in last 30 days
                contacts = db.query(Contact).filter(
                    Contact.created_at >= thirty_days_ago
                ).all()
            
            elif stage == 'active':
                # Opened email in last 30 days
                contacts = db.query(Contact).join(
                    EmailOpen, Contact.id == EmailOpen.contact_id
                ).filter(
                    EmailOpen.opened_at >= thirty_days_ago
                ).distinct().all()
            
            elif stage == 'at_risk':
                # Opened 30-90 days ago but not recently
                contacts = db.query(Contact).join(
                    EmailOpen, Contact.id == EmailOpen.contact_id
                ).filter(
                    EmailOpen.opened_at >= ninety_days_ago,
                    EmailOpen.opened_at < thirty_days_ago
                ).distinct().all()
            
            elif stage == 'churned':
                # No opens in last 90 days
                contacts = db.query(Contact).filter(
                    ~Contact.id.in_(
                        db.query(EmailOpen.contact_id).filter(
                            EmailOpen.opened_at >= ninety_days_ago
                        )
                    )
                ).all()
            
            else:
                contacts = []
            
            return contacts
        finally:
            db.close()
    
    def create_dynamic_segment(self, name: str, conditions: Dict) -> Dict:
        """Create a dynamic segment that updates automatically"""
        from segment_manager import SegmentManager
        segment_mgr = SegmentManager()
        
        # Build segment based on conditions
        contacts = []
        
        if 'behavior' in conditions:
            contacts = self.segment_by_behavior(
                conditions['behavior']['type'],
                conditions['behavior'].get('days', 30),
                conditions['behavior'].get('threshold', 1)
            )
        
        if 'lifecycle' in conditions:
            lifecycle_contacts = self.segment_by_lifecycle(conditions['lifecycle'])
            if contacts:
                # Intersection
                contacts = [c for c in contacts if c in lifecycle_contacts]
            else:
                contacts = lifecycle_contacts
        
        if 'demographics' in conditions:
            demo_contacts = self.segment_by_demographics(
                conditions['demographics']['field'],
                conditions['demographics']['value']
            )
            if contacts:
                contacts = [c for c in contacts if c in demo_contacts]
            else:
                contacts = demo_contacts
        
        # Create segment
        result = segment_mgr.create_segment(
            name=name,
            description=f"Dynamic segment: {conditions}",
            conditions=conditions
        )
        
        if result['status'] == 'success':
            # Add contacts to segment
            segment_id = result['segment'].id
            for contact in contacts:
                segment_mgr.add_to_segment(segment_id, contact.id)
        
        return result
    
    def get_segment_performance(self, segment_id: int) -> Dict:
        """Get performance metrics for a segment"""
        from segment_manager import SegmentManager
        segment_mgr = SegmentManager()
        
        contacts = segment_mgr.get_segment_contacts(segment_id)
        contact_ids = [c.id for c in contacts]
        
        db = get_db()
        try:
            # Get opens
            opens = db.query(EmailOpen).filter(
                EmailOpen.contact_id.in_(contact_ids)
            ).count()
            
            # Get clicks
            clicks = db.query(CampaignRecipient).filter(
                CampaignRecipient.contact_id.in_(contact_ids),
                CampaignRecipient.click_count > 0
            ).count()
            
            # Calculate rates
            open_rate = (opens / len(contacts) * 100) if contacts else 0
            click_rate = (clicks / len(contacts) * 100) if contacts else 0
            
            return {
                'segment_id': segment_id,
                'total_contacts': len(contacts),
                'total_opens': opens,
                'total_clicks': clicks,
                'open_rate': round(open_rate, 2),
                'click_rate': round(click_rate, 2)
            }
        finally:
            db.close()

