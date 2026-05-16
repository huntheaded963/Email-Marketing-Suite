"""
Campaign management module
"""
from database import get_db, Campaign, CampaignRecipient, Contact, ContactList, ContactListMember
from email_sender import EmailSender
from bounce_handler import BounceHandler
from unsubscribe_handler import UnsubscribeHandler
from tracking_hash import TrackingHashGenerator
from typing import List, Dict, Optional
from datetime import datetime
import time

class CampaignManager:
    """Manage email campaigns"""
    
    def __init__(self):
        self.email_sender = EmailSender()
        self.bounce_handler = BounceHandler()
        self.unsubscribe_handler = UnsubscribeHandler()
    
    def create_campaign(self, name: str, subject: str, body_html: str,
                      body_text: str = None, template_id: int = None) -> Dict:
        """Create a new campaign"""
        db = get_db()
        try:
            campaign = Campaign(
                name=name,
                subject=subject,
                body_html=body_html,
                body_text=body_text,
                template_id=template_id,
                status='draft'
            )
            db.add(campaign)
            db.commit()
            db.refresh(campaign)
            return {'status': 'success', 'campaign': campaign, 'message': 'Campaign created'}
        except Exception as e:
            db.rollback()
            return {'status': 'error', 'message': str(e)}
        finally:
            db.close()
    
    def get_campaign(self, campaign_id: int) -> Optional[Campaign]:
        """Get campaign by ID"""
        db = get_db()
        try:
            return db.query(Campaign).filter(Campaign.id == campaign_id).first()
        finally:
            db.close()
    
    def list_campaigns(self, status: str = None) -> List[Campaign]:
        """List all campaigns"""
        db = get_db()
        try:
            query = db.query(Campaign)
            if status:
                query = query.filter(Campaign.status == status)
            return query.order_by(Campaign.created_at.desc()).all()
        finally:
            db.close()
    
    def add_recipients(self, campaign_id: int, contact_ids: List[int] = None,
                      list_ids: List[int] = None, emails: List[str] = None) -> Dict:
        """Add recipients to a campaign"""
        db = get_db()
        try:
            campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
            if not campaign:
                return {'status': 'not_found', 'message': 'Campaign not found'}
            
            recipients_added = 0
            
            # Add by contact IDs
            if contact_ids:
                for contact_id in contact_ids:
                    existing = db.query(CampaignRecipient).filter(
                        CampaignRecipient.campaign_id == campaign_id,
                        CampaignRecipient.contact_id == contact_id
                    ).first()
                    if not existing:
                        recipient = CampaignRecipient(
                            campaign_id=campaign_id,
                            contact_id=contact_id,
                            status='pending'
                        )
                        db.add(recipient)
                        recipients_added += 1
            
            # Add by list IDs
            if list_ids:
                for list_id in list_ids:
                    members = db.query(ContactListMember).filter(
                        ContactListMember.list_id == list_id
                    ).all()
                    for member in members:
                        existing = db.query(CampaignRecipient).filter(
                            CampaignRecipient.campaign_id == campaign_id,
                            CampaignRecipient.contact_id == member.contact_id
                        ).first()
                        if not existing:
                            recipient = CampaignRecipient(
                                campaign_id=campaign_id,
                                contact_id=member.contact_id,
                                status='pending'
                            )
                            db.add(recipient)
                            recipients_added += 1
            
            # Add by email addresses
            if emails:
                for email in emails:
                    contact = db.query(Contact).filter(Contact.email == email).first()
                    if contact:
                        existing = db.query(CampaignRecipient).filter(
                            CampaignRecipient.campaign_id == campaign_id,
                            CampaignRecipient.contact_id == contact.id
                        ).first()
                        if not existing:
                            recipient = CampaignRecipient(
                                campaign_id=campaign_id,
                                contact_id=contact.id,
                                status='pending'
                            )
                            db.add(recipient)
                            recipients_added += 1
            
            db.commit()
            return {'status': 'success', 'recipients_added': recipients_added, 'message': f'{recipients_added} recipients added'}
        except Exception as e:
            db.rollback()
            return {'status': 'error', 'message': str(e)}
        finally:
            db.close()
    
    def send_campaign(self, campaign_id: int) -> Dict:
        """Send a campaign to all recipients"""
        db = get_db()
        try:
            campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
            if not campaign:
                return {'status': 'not_found', 'message': 'Campaign not found'}
            
            # Update campaign status
            campaign.status = 'sending'
            campaign.sent_at = datetime.utcnow()
            db.commit()
            
            # Get all pending recipients
            recipients = db.query(CampaignRecipient).filter(
                CampaignRecipient.campaign_id == campaign_id,
                CampaignRecipient.status == 'pending'
            ).all()
            
            if not recipients:
                return {'status': 'no_recipients', 'message': 'No recipients found'}
            
            results = {'sent': 0, 'failed': 0, 'skipped': 0}
            
            for recipient in recipients:
                contact = recipient.contact
                
                # Skip unsubscribed contacts
                if contact.status == 'unsubscribed' or self.unsubscribe_handler.is_unsubscribed(contact.email):
                    recipient.status = 'unsubscribed'
                    results['skipped'] += 1
                    db.commit()
                    continue
                
                # Skip bounced contacts
                if self.bounce_handler.is_bounced(contact.email):
                    recipient.status = 'bounced'
                    results['skipped'] += 1
                    db.commit()
                    continue
                
                # Generate tracking hash and unsubscribe hash
                tracking_hash = TrackingHashGenerator.get_or_create_hash(
                    email=contact.email,
                    campaign_id=campaign_id,
                    contact_id=contact.id
                )
                unsubscribe_hash = self.unsubscribe_handler.generate_unsubscribe_hash(contact.email)
                
                # Replace template variables
                email_html = campaign.body_html
                email_html = email_html.replace('{TRACKING_PIXEL}', 
                    f'<img src="http://localhost:8080/track.php?mb={tracking_hash}" width="1" height="1" style="display:none;">')
                email_html = email_html.replace('{TRACKING_LINK}', f'http://localhost:8080/track.php?mb={tracking_hash}')
                email_html = email_html.replace('{EMAIL}', contact.email)
                email_html = email_html.replace('{HASH}', unsubscribe_hash)
                email_html = email_html.replace('{NAME}', f"{contact.first_name or ''} {contact.last_name or ''}".strip() or 'User')
                
                # Send email with tracking
                result = self.email_sender.send_email(
                    to_email=contact.email,
                    subject=campaign.subject,
                    body_html=email_html,
                    body_text=campaign.body_text,
                    tracking_pixel=True,
                    campaign_id=campaign_id,
                    contact_id=contact.id
                )
                
                if result['status'] == 'success':
                    recipient.status = 'sent'
                    recipient.sent_at = datetime.utcnow()
                    results['sent'] += 1
                else:
                    recipient.status = 'failed'
                    results['failed'] += 1
                    # Check if it's a bounce
                    error_msg = result.get('error', '').lower()
                    if 'bounce' in error_msg or 'rejected' in error_msg or 'invalid' in error_msg:
                        self.bounce_handler.record_bounce(
                            email=contact.email,
                            bounce_type='soft',
                            bounce_reason=result.get('error'),
                            campaign_id=campaign_id,
                            contact_id=contact.id
                        )
                
                db.commit()
                time.sleep(0.5)  # Rate limiting
            
            # Update campaign status
            campaign.status = 'sent'
            db.commit()
            
            return {'status': 'success', 'results': results, 'message': f"Campaign sent: {results['sent']} sent, {results['failed']} failed"}
        except Exception as e:
            db.rollback()
            campaign.status = 'failed'
            db.commit()
            return {'status': 'error', 'message': str(e)}
        finally:
            db.close()
    
    def schedule_campaign(self, campaign_id: int, scheduled_at: datetime) -> Dict:
        """Schedule a campaign for later sending"""
        db = get_db()
        try:
            campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
            if not campaign:
                return {'status': 'not_found', 'message': 'Campaign not found'}
            
            campaign.scheduled_at = scheduled_at
            campaign.status = 'scheduled'
            db.commit()
            
            return {'status': 'success', 'message': f'Campaign scheduled for {scheduled_at}'}
        except Exception as e:
            db.rollback()
            return {'status': 'error', 'message': str(e)}
        finally:
            db.close()
    
    def get_campaign_stats(self, campaign_id: int) -> Dict:
        """Get campaign statistics"""
        db = get_db()
        try:
            recipients = db.query(CampaignRecipient).filter(
                CampaignRecipient.campaign_id == campaign_id
            ).all()
            
            stats = {
                'total': len(recipients),
                'pending': 0,
                'sent': 0,
                'delivered': 0,
                'opened': 0,
                'clicked': 0,
                'bounced': 0,
                'failed': 0,
                'open_rate': 0,
                'click_rate': 0
            }
            
            for recipient in recipients:
                stats[recipient.status] = stats.get(recipient.status, 0) + 1
                if recipient.open_count > 0:
                    stats['opened'] += 1
                if recipient.click_count > 0:
                    stats['clicked'] += 1
            
            if stats['sent'] > 0:
                stats['open_rate'] = (stats['opened'] / stats['sent']) * 100
                stats['click_rate'] = (stats['clicked'] / stats['sent']) * 100
            
            return {'status': 'success', 'stats': stats}
        finally:
            db.close()

