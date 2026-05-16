"""
Email sending module with SMTP support
"""
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Dict, Optional
from config import Config
from tracking_hash import TrackingHashGenerator
from tracking_server import get_tracking_server
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailSender:
    """Handle email sending via SMTP"""
    
    def __init__(self):
        self.smtp_host = Config.SMTP_HOST
        self.smtp_port = Config.SMTP_PORT
        self.smtp_user = Config.SMTP_USER
        self.smtp_password = Config.SMTP_PASSWORD
        self.use_tls = Config.SMTP_USE_TLS
        self.max_batch = Config.MAX_EMAILS_PER_BATCH
        self.delay = Config.DELAY_BETWEEN_EMAILS
        
    def _create_message(self, to_email: str, subject: str, body_html: str, 
                       body_text: str = None, from_email: str = None,
                       reply_to: str = None, tracking_pixel: bool = False,
                       campaign_id: int = None, contact_id: int = None) -> MIMEMultipart:
        """Create email message"""
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['To'] = to_email
        msg['From'] = from_email or self.smtp_user
        
        if reply_to:
            msg['Reply-To'] = reply_to
        
        # Add tracking pixel if enabled
        if tracking_pixel and campaign_id and contact_id:
            # Generate or get tracking hash
            hash_value = TrackingHashGenerator.get_or_create_hash(
                email=to_email,
                campaign_id=campaign_id,
                contact_id=contact_id
            )
            
            # Get tracking server URL
            tracking_server = get_tracking_server()
            tracking_url = tracking_server.get_tracking_url(hash_value)
            
            # Add tracking pixel to HTML (invisible 1x1 image)
            # Insert before closing body tag, or at the end if no body tag
            if '</body>' in body_html:
                body_html = body_html.replace('</body>', 
                    f'<img src="{tracking_url}" width="1" height="1" style="display:none;"></body>')
            else:
                body_html += f'<img src="{tracking_url}" width="1" height="1" style="display:none;">'
        
        # Add text version
        if body_text:
            part1 = MIMEText(body_text, 'plain')
            msg.attach(part1)
        
        # Add HTML version
        part2 = MIMEText(body_html, 'html')
        msg.attach(part2)
        
        return msg
    
    def send_email(self, to_email: str, subject: str, body_html: str,
                   body_text: str = None, from_email: str = None,
                   reply_to: str = None, tracking_pixel: bool = False,
                   campaign_id: int = None, contact_id: int = None) -> Dict[str, any]:
        """Send single email"""
        try:
            msg = self._create_message(to_email, subject, body_html, body_text,
                                     from_email, reply_to, tracking_pixel, campaign_id, contact_id)
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {to_email}")
            return {'status': 'success', 'email': to_email, 'error': None}
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return {'status': 'failed', 'email': to_email, 'error': str(e)}
    
    def send_bulk(self, recipients: List[Dict], subject: str, body_html: str,
                  body_text: str = None, from_email: str = None,
                  tracking_pixel: bool = False, campaign_id: int = None) -> List[Dict]:
        """Send bulk emails with rate limiting"""
        results = []
        total = len(recipients)
        
        logger.info(f"Starting bulk email send to {total} recipients")
        
        for i, recipient in enumerate(recipients, 1):
            to_email = recipient.get('email') or recipient.get('to')
            
            result = self.send_email(
                to_email=to_email,
                subject=subject,
                body_html=body_html,
                body_text=body_text,
                from_email=from_email,
                tracking_pixel=tracking_pixel,
                campaign_id=campaign_id
            )
            results.append(result)
            
            # Progress logging
            if i % 10 == 0:
                logger.info(f"Progress: {i}/{total} emails sent")
            
            # Rate limiting
            if i < total and self.delay > 0:
                time.sleep(self.delay)
        
        success_count = sum(1 for r in results if r['status'] == 'success')
        logger.info(f"Bulk send complete: {success_count}/{total} successful")
        
        return results
    
    def test_connection(self) -> bool:
        """Test SMTP connection with detailed error logging"""
        try:
            logger.info(f"Testing SMTP connection to {self.smtp_host}:{self.smtp_port}")
            
            # Test connection
            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=15) as server:
                if self.use_tls:
                    logger.info("Starting TLS...")
                    server.starttls()
                
                logger.info(f"Authenticating as {self.smtp_user}...")
                server.login(self.smtp_user, self.smtp_password)
            
            logger.info("SMTP connection test successful")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP authentication failed: {str(e)}")
            logger.error("Check your username and password")
            return False
        except smtplib.SMTPConnectError as e:
            logger.error(f"SMTP connection error: {str(e)}")
            logger.error("Check host and port settings")
            return False
        except Exception as e:
            logger.error(f"SMTP connection test failed: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            return False

