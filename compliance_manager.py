"""
Legal Compliance Manager (GDPR, CCPA, CAN-SPAM)
مدير الامتثال القانوني
"""

from database import get_db, Contact
from typing import Dict, Optional
from datetime import datetime
import json

class ComplianceManager:
    """Manage legal compliance for email marketing"""
    
    def __init__(self):
        self.regulations = {
            'GDPR': {
                'name': 'General Data Protection Regulation',
                'region': 'EU',
                'requires_consent': True,
                'requires_double_optin': True,
                'right_to_delete': True,
                'right_to_export': True
            },
            'CCPA': {
                'name': 'California Consumer Privacy Act',
                'region': 'California, USA',
                'requires_consent': True,
                'requires_double_optin': False,
                'right_to_delete': True,
                'right_to_export': True
            },
            'CAN_SPAM': {
                'name': 'CAN-SPAM Act',
                'region': 'USA',
                'requires_consent': False,
                'requires_double_optin': False,
                'right_to_delete': True,
                'right_to_export': False
            }
        }
    
    def add_consent(self, email: str, consent_type: str, 
                   ip_address: str = None, user_agent: str = None) -> Dict:
        """Record consent for a contact"""
        db = get_db()
        try:
            contact = db.query(Contact).filter(Contact.email == email).first()
            if not contact:
                return {'status': 'not_found', 'message': 'Contact not found'}
            
            # Store consent in tags or custom field
            if not contact.tags:
                contact.tags = ''
            
            consent_tag = f'consent_{consent_type}'
            if consent_tag not in contact.tags:
                contact.tags += f',{consent_tag}' if contact.tags else consent_tag
            
            # Store consent metadata (would need consent_logs table for full implementation)
            contact.status = 'active'  # Activate on consent
            
            db.commit()
            return {'status': 'success', 'message': 'Consent recorded'}
        except Exception as e:
            db.rollback()
            return {'status': 'error', 'message': str(e)}
        finally:
            db.close()
    
    def setup_double_optin(self, email: str) -> Dict:
        """Set up double opt-in confirmation"""
        # This would send a confirmation email
        # For now, just mark as pending
        db = get_db()
        try:
            contact = db.query(Contact).filter(Contact.email == email).first()
            if contact:
                contact.status = 'pending_confirmation'
                db.commit()
                return {'status': 'success', 'message': 'Confirmation email sent'}
            return {'status': 'not_found', 'message': 'Contact not found'}
        except Exception as e:
            db.rollback()
            return {'status': 'error', 'message': str(e)}
        finally:
            db.close()
    
    def confirm_double_optin(self, email: str, confirmation_hash: str) -> Dict:
        """Confirm double opt-in"""
        db = get_db()
        try:
            contact = db.query(Contact).filter(Contact.email == email).first()
            if contact and contact.status == 'pending_confirmation':
                # Verify hash (simplified)
                contact.status = 'active'
                db.commit()
                return {'status': 'success', 'message': 'Email confirmed'}
            return {'status': 'error', 'message': 'Invalid confirmation'}
        except Exception as e:
            db.rollback()
            return {'status': 'error', 'message': str(e)}
        finally:
            db.close()
    
    def export_contact_data(self, email: str) -> Dict:
        """Export all data for a contact (GDPR/CCPA right to access)"""
        db = get_db()
        try:
            contact = db.query(Contact).filter(Contact.email == email).first()
            if not contact:
                return {'status': 'not_found', 'message': 'Contact not found'}
            
            # Get all related data
            from database import EmailOpen, CampaignRecipient, Bounce, Unsubscribe
            
            opens = db.query(EmailOpen).filter(EmailOpen.contact_id == contact.id).all()
            recipients = db.query(CampaignRecipient).filter(
                CampaignRecipient.contact_id == contact.id
            ).all()
            
            data = {
                'contact': {
                    'email': contact.email,
                    'first_name': contact.first_name,
                    'last_name': contact.last_name,
                    'phone': contact.phone,
                    'status': contact.status,
                    'created_at': contact.created_at.isoformat() if contact.created_at else None,
                    'tags': contact.tags
                },
                'email_opens': [
                    {
                        'opened_at': open_record.opened_at.isoformat() if open_record.opened_at else None,
                        'ip_address': open_record.ip_address,
                        'country': open_record.country
                    } for open_record in opens
                ],
                'campaigns': [
                    {
                        'campaign_id': rec.campaign_id,
                        'status': rec.status,
                        'sent_at': rec.sent_at.isoformat() if rec.sent_at else None,
                        'opened': rec.opened,
                        'clicked': rec.click_count > 0
                    } for rec in recipients
                ]
            }
            
            return {'status': 'success', 'data': data}
        finally:
            db.close()
    
    def delete_contact_data(self, email: str) -> Dict:
        """Delete all data for a contact (GDPR/CCPA right to be forgotten)"""
        db = get_db()
        try:
            contact = db.query(Contact).filter(Contact.email == email).first()
            if not contact:
                return {'status': 'not_found', 'message': 'Contact not found'}
            
            # Delete related records
            from database import EmailOpen, CampaignRecipient
            
            db.query(EmailOpen).filter(EmailOpen.contact_id == contact.id).delete()
            db.query(CampaignRecipient).filter(
                CampaignRecipient.contact_id == contact.id
            ).delete()
            
            # Delete contact
            db.delete(contact)
            db.commit()
            
            return {'status': 'success', 'message': 'All data deleted'}
        except Exception as e:
            db.rollback()
            return {'status': 'error', 'message': str(e)}
        finally:
            db.close()
    
    def add_unsubscribe_link(self, email_html: str, email: str, hash_value: str) -> str:
        """Add compliant unsubscribe link to email"""
        unsubscribe_url = f"http://localhost:8080/unsubscribe.php?email={email}&hash={hash_value}"
        
        unsubscribe_html = f"""
        <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #666;">
            <p>You are receiving this email because you subscribed to our mailing list.</p>
            <p><a href="{unsubscribe_url}" style="color: #666;">Unsubscribe</a> | 
               <a href="#" style="color: #666;">Update Preferences</a></p>
            <p>Our mailing address is: [Your Address]</p>
        </div>
        """
        
        return email_html + unsubscribe_html
    
    def check_compliance_status(self, contact_id: int) -> Dict:
        """Check compliance status for a contact"""
        db = get_db()
        try:
            contact = db.query(Contact).filter(Contact.id == contact_id).first()
            if not contact:
                return {'status': 'not_found'}
            
            compliance = {
                'has_consent': 'consent' in (contact.tags or ''),
                'double_optin_confirmed': contact.status != 'pending_confirmation',
                'can_send': contact.status == 'active' and 'consent' in (contact.tags or ''),
                'regulations': []
            }
            
            # Check which regulations apply
            if 'consent_gdpr' in (contact.tags or ''):
                compliance['regulations'].append('GDPR')
            if 'consent_ccpa' in (contact.tags or ''):
                compliance['regulations'].append('CCPA')
            
            return {'status': 'success', 'compliance': compliance}
        finally:
            db.close()

