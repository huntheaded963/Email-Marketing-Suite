"""
SMTP Providers Configuration - All Major Email Providers
إعدادات جميع مزودي SMTP في العالم
"""

from typing import Dict, List, Optional

class SMTPProviders:
    """All major SMTP providers configuration"""
    
    def __init__(self):
        self.providers = self._initialize_providers()
    
    def _initialize_providers(self) -> Dict:
        """Initialize all SMTP providers"""
        return {
            # Gmail
            'gmail': {
                'name': 'Gmail',
                'host': 'smtp.gmail.com',
                'port': 587,
                'ssl': False,
                'tls': True,
                'auth': True,
                'note': 'Requires App Password (not regular password). Enable 2FA first.',
                'website': 'https://mail.google.com'
            },
            'gmail_ssl': {
                'name': 'Gmail (SSL)',
                'host': 'smtp.gmail.com',
                'port': 465,
                'ssl': True,
                'tls': False,
                'auth': True
            },
            
            # Outlook / Hotmail / Office 365
            'outlook': {
                'name': 'Outlook.com',
                'host': 'smtp-mail.outlook.com',
                'port': 587,
                'ssl': False,
                'tls': True,
                'auth': True
            },
            'office365': {
                'name': 'Office 365',
                'host': 'smtp.office365.com',
                'port': 587,
                'ssl': False,
                'tls': True,
                'auth': True
            },
            
            # Yahoo
            'yahoo': {
                'name': 'Yahoo Mail',
                'host': 'smtp.mail.yahoo.com',
                'port': 587,
                'ssl': False,
                'tls': True,
                'auth': True,
                'note': 'Requires App Password'
            },
            'yahoo_ssl': {
                'name': 'Yahoo Mail (SSL)',
                'host': 'smtp.mail.yahoo.com',
                'port': 465,
                'ssl': True,
                'tls': False,
                'auth': True
            },
            
            # AOL
            'aol': {
                'name': 'AOL Mail',
                'host': 'smtp.aol.com',
                'port': 587,
                'ssl': False,
                'tls': True,
                'auth': True
            },
            
            # Zoho
            'zoho': {
                'name': 'Zoho Mail',
                'host': 'smtp.zoho.com',
                'port': 587,
                'ssl': False,
                'tls': True,
                'auth': True
            },
            'zoho_eu': {
                'name': 'Zoho Mail (EU)',
                'host': 'smtp.zoho.eu',
                'port': 587,
                'ssl': False,
                'tls': True,
                'auth': True
            },
            'zoho_ssl': {
                'name': 'Zoho Mail (SSL)',
                'host': 'smtp.zoho.com',
                'port': 465,
                'ssl': True,
                'tls': False,
                'auth': True
            },
            
            # ProtonMail
            'protonmail': {
                'name': 'ProtonMail',
                'host': 'mail.protonmail.com',
                'port': 587,
                'ssl': False,
                'tls': True,
                'auth': True,
                'note': 'Requires ProtonMail Bridge'
            },
            
            # Mail.com
            'mail_com': {
                'name': 'Mail.com',
                'host': 'smtp.mail.com',
                'port': 587,
                'ssl': False,
                'tls': True,
                'auth': True
            },
            
            # GMX
            'gmx': {
                'name': 'GMX',
                'host': 'mail.gmx.com',
                'port': 587,
                'ssl': False,
                'tls': True,
                'auth': True
            },
            'gmx_ssl': {
                'name': 'GMX (SSL)',
                'host': 'mail.gmx.com',
                'port': 465,
                'ssl': True,
                'tls': False,
                'auth': True
            },
            
            # Yandex
            'yandex': {
                'name': 'Yandex Mail',
                'host': 'smtp.yandex.com',
                'port': 587,
                'ssl': False,
                'tls': True,
                'auth': True
            },
            'yandex_ssl': {
                'name': 'Yandex Mail (SSL)',
                'host': 'smtp.yandex.com',
                'port': 465,
                'ssl': True,
                'tls': False,
                'auth': True
            },
            
            # Mail.ru
            'mail_ru': {
                'name': 'Mail.ru',
                'host': 'smtp.mail.ru',
                'port': 587,
                'ssl': False,
                'tls': True,
                'auth': True
            },
            'mail_ru_ssl': {
                'name': 'Mail.ru (SSL)',
                'host': 'smtp.mail.ru',
                'port': 465,
                'ssl': True,
                'tls': False,
                'auth': True
            },
            
            # QQ Mail (China)
            'qq': {
                'name': 'QQ Mail',
                'host': 'smtp.qq.com',
                'port': 587,
                'ssl': False,
                'tls': True,
                'auth': True,
                'note': 'Requires authorization code'
            },
            'qq_ssl': {
                'name': 'QQ Mail (SSL)',
                'host': 'smtp.qq.com',
                'port': 465,
                'ssl': True,
                'tls': False,
                'auth': True
            },
            
            # 163 Mail (China)
            '163': {
                'name': '163 Mail',
                'host': 'smtp.163.com',
                'port': 25,
                'ssl': False,
                'tls': True,
                'auth': True
            },
            '163_ssl': {
                'name': '163 Mail (SSL)',
                'host': 'smtp.163.com',
                'port': 465,
                'ssl': True,
                'tls': False,
                'auth': True
            },
            
            # Sina Mail (China)
            'sina': {
                'name': 'Sina Mail',
                'host': 'smtp.sina.com',
                'port': 25,
                'ssl': False,
                'tls': True,
                'auth': True
            },
            
            # SendGrid
            'sendgrid': {
                'name': 'SendGrid',
                'host': 'smtp.sendgrid.net',
                'port': 587,
                'ssl': False,
                'tls': True,
                'auth': True,
                'note': 'Use API key as password'
            },
            
            # Mailgun
            'mailgun': {
                'name': 'Mailgun',
                'host': 'smtp.mailgun.org',
                'port': 587,
                'ssl': False,
                'tls': True,
                'auth': True,
                'note': 'Use SMTP credentials from Mailgun dashboard'
            },
            
            # Amazon SES
            'amazon_ses': {
                'name': 'Amazon SES',
                'host': 'email-smtp.us-east-1.amazonaws.com',
                'port': 587,
                'ssl': False,
                'tls': True,
                'auth': True,
                'note': 'Use region-specific host. Replace us-east-1 with your region'
            },
            'amazon_ses_ssl': {
                'name': 'Amazon SES (SSL)',
                'host': 'email-smtp.us-east-1.amazonaws.com',
                'port': 465,
                'ssl': True,
                'tls': False,
                'auth': True
            },
            
            # Mailjet
            'mailjet': {
                'name': 'Mailjet',
                'host': 'in-v3.mailjet.com',
                'port': 587,
                'ssl': False,
                'tls': True,
                'auth': True
            },
            
            # Brevo (formerly Sendinblue)
            'brevo': {
                'name': 'Brevo (Sendinblue)',
                'host': 'smtp-relay.brevo.com',
                'port': 587,
                'ssl': False,
                'tls': True,
                'auth': True
            },
            
            # Postmark
            'postmark': {
                'name': 'Postmark',
                'host': 'smtp.postmarkapp.com',
                'port': 587,
                'ssl': False,
                'tls': True,
                'auth': True
            },
            
            # SparkPost
            'sparkpost': {
                'name': 'SparkPost',
                'host': 'smtp.sparkpostmail.com',
                'port': 587,
                'ssl': False,
                'tls': True,
                'auth': True
            },
            
            # Mandrill
            'mandrill': {
                'name': 'Mandrill',
                'host': 'smtp.mandrillapp.com',
                'port': 587,
                'ssl': False,
                'tls': True,
                'auth': True
            },
            
            # Mailchimp Transactional
            'mailchimp': {
                'name': 'Mailchimp Transactional',
                'host': 'smtp.mandrillapp.com',
                'port': 587,
                'ssl': False,
                'tls': True,
                'auth': True
            },
            
            # Elastic Email
            'elastic_email': {
                'name': 'Elastic Email',
                'host': 'smtp.elasticemail.com',
                'port': 2525,
                'ssl': False,
                'tls': True,
                'auth': True
            },
            'elastic_email_ssl': {
                'name': 'Elastic Email (SSL)',
                'host': 'smtp.elasticemail.com',
                'port': 465,
                'ssl': True,
                'tls': False,
                'auth': True
            },
            
            # Pepipost
            'pepipost': {
                'name': 'Pepipost',
                'host': 'smtp.pepipost.com',
                'port': 587,
                'ssl': False,
                'tls': True,
                'auth': True
            },
            
            # SocketLabs
            'socketlabs': {
                'name': 'SocketLabs',
                'host': 'smtp.socketlabs.com',
                'port': 587,
                'ssl': False,
                'tls': True,
                'auth': True
            },
            
            # Postfix (Custom)
            'postfix': {
                'name': 'Postfix (Custom Server)',
                'host': 'localhost',
                'port': 25,
                'ssl': False,
                'tls': False,
                'auth': False,
                'note': 'Local Postfix server'
            },
            
            # Exim (Custom)
            'exim': {
                'name': 'Exim (Custom Server)',
                'host': 'localhost',
                'port': 25,
                'ssl': False,
                'tls': False,
                'auth': False,
                'note': 'Local Exim server'
            },
            
            # iCloud
            'icloud': {
                'name': 'iCloud Mail',
                'host': 'smtp.mail.me.com',
                'port': 587,
                'ssl': False,
                'tls': True,
                'auth': True,
                'note': 'Requires App-Specific Password'
            },
            
            # FastMail
            'fastmail': {
                'name': 'FastMail',
                'host': 'smtp.fastmail.com',
                'port': 587,
                'ssl': False,
                'tls': True,
                'auth': True
            },
            
            # Tutanota
            'tutanota': {
                'name': 'Tutanota',
                'host': 'smtp.tutanota.com',
                'port': 587,
                'ssl': False,
                'tls': True,
                'auth': True
            },
            
            # Hushmail
            'hushmail': {
                'name': 'Hushmail',
                'host': 'smtp.hushmail.com',
                'port': 587,
                'ssl': False,
                'tls': True,
                'auth': True
            },
            
            # Custom SMTP
            'custom': {
                'name': 'Custom SMTP',
                'host': '',
                'port': 587,
                'ssl': False,
                'tls': True,
                'auth': True,
                'note': 'Enter your custom SMTP settings'
            }
        }
    
    def get_provider(self, provider_key: str) -> Optional[Dict]:
        """Get provider configuration"""
        return self.providers.get(provider_key.lower())
    
    def get_all_providers(self) -> Dict:
        """Get all providers"""
        return self.providers
    
    def get_provider_list(self) -> List[Dict]:
        """Get list of all providers with details"""
        providers_list = []
        for key, config in self.providers.items():
            providers_list.append({
                'key': key,
                'name': config['name'],
                'host': config['host'],
                'port': config['port'],
                'ssl': config.get('ssl', False),
                'tls': config.get('tls', False),
                'note': config.get('note', '')
            })
        return providers_list
    
    def search_providers(self, query: str) -> List[Dict]:
        """Search providers by name"""
        query_lower = query.lower()
        results = []
        for key, config in self.providers.items():
            if query_lower in config['name'].lower() or query_lower in key.lower():
                results.append({
                    'key': key,
                    'name': config['name'],
                    'host': config['host'],
                    'port': config['port']
                })
        return results
    
    def get_provider_by_host(self, host: str) -> Optional[Dict]:
        """Get provider by SMTP host"""
        for key, config in self.providers.items():
            if config['host'].lower() == host.lower():
                return {'key': key, **config}
        return None
    
    def get_providers_by_category(self) -> Dict:
        """Get providers grouped by category"""
        categories = {
            'Personal Email': ['gmail', 'outlook', 'yahoo', 'aol', 'icloud'],
            'Business Email': ['office365', 'zoho', 'gmx', 'mail_com'],
            'Privacy-Focused': ['protonmail', 'tutanota', 'hushmail', 'fastmail'],
            'Transactional Services': ['sendgrid', 'mailgun', 'amazon_ses', 'mailjet', 
                                      'brevo', 'postmark', 'sparkpost', 'mandrill',
                                      'elastic_email', 'pepipost', 'socketlabs'],
            'Regional': ['yandex', 'mail_ru', 'qq', '163', 'sina'],
            'Custom Servers': ['postfix', 'exim', 'custom']
        }
        
        result = {}
        for category, provider_keys in categories.items():
            result[category] = []
            for key in provider_keys:
                if key in self.providers:
                    result[category].append({
                        'key': key,
                        'name': self.providers[key]['name'],
                        'host': self.providers[key]['host'],
                        'port': self.providers[key]['port']
                    })
        
        return result

