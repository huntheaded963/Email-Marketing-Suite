"""
Advanced List Hygiene Management
إدارة تنظيف القوائم المتقدمة
"""

from database import get_db, Contact, Bounce, Unsubscribe, EmailOpen, CampaignRecipient
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from sqlalchemy import func, and_, or_

class ListHygieneManager:
    """Advanced list hygiene and suppression management"""
    
    def __init__(self):
        self.suppression_reasons = {
            'hard_bounce': 'Hard bounce detected',
            'soft_bounce': 'Soft bounce (multiple failures)',
            'spam_complaint': 'Spam complaint received',
            'unsubscribed': 'User unsubscribed',
            'invalid_email': 'Invalid email format',
            'role_based': 'Role-based email (info@, support@, etc.)',
            'temporary_domain': 'Temporary/disposable email domain',
            'inactive': 'Inactive for extended period',
            'low_engagement': 'Low engagement score'
        }
    
    def identify_suppression_candidates(self, days_inactive: int = 90, 
                                       min_opens: int = 0) -> List[Contact]:
        """Identify contacts that should be suppressed"""
        db = get_db()
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_inactive)
            
            # Find inactive contacts
            inactive_contacts = db.query(Contact).filter(
                Contact.status == 'active',
                ~Contact.id.in_(
                    db.query(EmailOpen.contact_id).filter(
                        EmailOpen.opened_at >= cutoff_date
                    )
                )
            ).all()
            
            # Find low engagement contacts
            low_engagement = db.query(Contact).join(
                EmailOpen, Contact.id == EmailOpen.contact_id
            ).group_by(Contact.id).having(
                func.count(EmailOpen.id) < min_opens
            ).all()
            
            # Combine and deduplicate
            candidates = list(set(inactive_contacts + low_engagement))
            
            return candidates
        finally:
            db.close()
    
    def check_email_quality(self, email: str) -> Dict:
        """Check email quality and flag potential issues"""
        issues = []
        risk_score = 0
        
        # Check for role-based emails
        role_based = ['info@', 'support@', 'contact@', 'sales@', 'admin@', 
                     'noreply@', 'no-reply@', 'postmaster@', 'webmaster@']
        if any(email.lower().startswith(role) for role in role_based):
            issues.append('role_based')
            risk_score += 30
        
        # Check for temporary/disposable domains
        disposable_domains = ['tempmail.com', '10minutemail.com', 'guerrillamail.com',
                            'mailinator.com', 'throwaway.email', 'temp-mail.org']
        domain = email.split('@')[1].lower() if '@' in email else ''
        if any(disposable in domain for disposable in disposable_domains):
            issues.append('temporary_domain')
            risk_score += 50
        
        # Check format
        if '@' not in email or '.' not in email.split('@')[1]:
            issues.append('invalid_email')
            risk_score += 100
        
        # Check for suspicious patterns
        if email.count('@') > 1 or email.count('..') > 0:
            issues.append('invalid_format')
            risk_score += 50
        
        return {
            'email': email,
            'risk_score': risk_score,
            'issues': issues,
            'is_safe': risk_score < 50
        }
    
    def get_suppression_list(self, reason: str = None) -> List[Dict]:
        """Get suppression list with reasons"""
        db = get_db()
        try:
            suppressions = []
            
            # Hard bounces
            if not reason or reason == 'hard_bounce':
                hard_bounces = db.query(Bounce).filter(
                    Bounce.bounce_type == 'hard'
                ).all()
                for bounce in hard_bounces:
                    suppressions.append({
                        'email': bounce.email,
                        'reason': 'hard_bounce',
                        'date': bounce.bounced_at,
                        'details': bounce.bounce_reason
                    })
            
            # Unsubscribes
            if not reason or reason == 'unsubscribed':
                unsubscribes = db.query(Unsubscribe).all()
                for unsub in unsubscribes:
                    suppressions.append({
                        'email': unsub.email,
                        'reason': 'unsubscribed',
                        'date': unsub.unsubscribed_at,
                        'details': unsub.reason
                    })
            
            # Spam complaints (if tracked)
            if not reason or reason == 'spam_complaint':
                # This would need a spam_complaints table
                pass
            
            return suppressions
        finally:
            db.close()
    
    def suppress_contact(self, email: str, reason: str, details: str = None) -> Dict:
        """Suppress a contact from future sends"""
        db = get_db()
        try:
            contact = db.query(Contact).filter(Contact.email == email).first()
            if not contact:
                return {'status': 'not_found', 'message': 'Contact not found'}
            
            # Update contact status
            if reason == 'hard_bounce':
                contact.status = 'bounced'
            elif reason == 'unsubscribed':
                contact.status = 'unsubscribed'
            elif reason == 'spam_complaint':
                contact.status = 'suppressed'
            else:
                contact.status = 'suppressed'
            
            # Add tag for tracking
            if not contact.tags:
                contact.tags = ''
            if 'suppressed' not in contact.tags:
                contact.tags += ',suppressed' if contact.tags else 'suppressed'
            
            db.commit()
            return {'status': 'success', 'message': f'Contact suppressed: {reason}'}
        except Exception as e:
            db.rollback()
            return {'status': 'error', 'message': str(e)}
        finally:
            db.close()
    
    def get_list_health_score(self) -> Dict:
        """Calculate overall list health score"""
        db = get_db()
        try:
            total_contacts = db.query(Contact).count()
            active_contacts = db.query(Contact).filter(Contact.status == 'active').count()
            bounced = db.query(Contact).filter(Contact.status == 'bounced').count()
            unsubscribed = db.query(Contact).filter(Contact.status == 'unsubscribed').count()
            suppressed = db.query(Contact).filter(Contact.status == 'suppressed').count()
            
            # Calculate health metrics
            active_rate = (active_contacts / total_contacts * 100) if total_contacts > 0 else 0
            bounce_rate = (bounced / total_contacts * 100) if total_contacts > 0 else 0
            unsubscribe_rate = (unsubscribed / total_contacts * 100) if total_contacts > 0 else 0
            
            # Health score (0-100)
            health_score = active_rate - (bounce_rate * 2) - (unsubscribe_rate * 1.5)
            health_score = max(0, min(100, health_score))
            
            # Get recent engagement
            recent_opens = db.query(EmailOpen).filter(
                EmailOpen.opened_at >= datetime.utcnow() - timedelta(days=30)
            ).count()
            
            engagement_rate = (recent_opens / active_contacts * 100) if active_contacts > 0 else 0
            
            return {
                'total_contacts': total_contacts,
                'active_contacts': active_contacts,
                'bounced': bounced,
                'unsubscribed': unsubscribed,
                'suppressed': suppressed,
                'active_rate': round(active_rate, 2),
                'bounce_rate': round(bounce_rate, 2),
                'unsubscribe_rate': round(unsubscribe_rate, 2),
                'health_score': round(health_score, 2),
                'engagement_rate': round(engagement_rate, 2),
                'status': 'excellent' if health_score >= 80 else 'good' if health_score >= 60 else 'fair' if health_score >= 40 else 'poor'
            }
        finally:
            db.close()
    
    def cleanup_inactive_contacts(self, days_inactive: int = 180, 
                                  action: str = 'suppress') -> Dict:
        """Clean up inactive contacts"""
        candidates = self.identify_suppression_candidates(days_inactive=days_inactive)
        
        results = {'processed': 0, 'suppressed': 0, 'errors': 0}
        
        for contact in candidates:
            try:
                if action == 'suppress':
                    result = self.suppress_contact(contact.email, 'inactive', 
                                                 f'Inactive for {days_inactive} days')
                    if result['status'] == 'success':
                        results['suppressed'] += 1
                elif action == 'delete':
                    # Delete contact (use with caution)
                    db = get_db()
                    try:
                        db.delete(contact)
                        db.commit()
                        results['suppressed'] += 1
                    finally:
                        db.close()
                
                results['processed'] += 1
            except Exception as e:
                results['errors'] += 1
        
        return results

