"""
Email template management module
"""
from database import get_db, EmailTemplate
from typing import List, Dict, Optional
from jinja2 import Template

class TemplateManager:
    """Manage email templates"""
    
    def create_template(self, name: str, subject: str, body_html: str,
                       body_text: str = None) -> Dict:
        """Create a new email template"""
        db = get_db()
        try:
            template = EmailTemplate(
                name=name,
                subject=subject,
                body_html=body_html,
                body_text=body_text
            )
            db.add(template)
            db.commit()
            db.refresh(template)
            return {'status': 'success', 'template': template, 'message': 'Template created'}
        except Exception as e:
            db.rollback()
            return {'status': 'error', 'message': str(e)}
        finally:
            db.close()
    
    def get_template(self, template_id: int) -> Optional[EmailTemplate]:
        """Get template by ID"""
        db = get_db()
        try:
            return db.query(EmailTemplate).filter(EmailTemplate.id == template_id).first()
        finally:
            db.close()
    
    def list_templates(self) -> List[EmailTemplate]:
        """List all templates"""
        db = get_db()
        try:
            return db.query(EmailTemplate).all()
        finally:
            db.close()
    
    def update_template(self, template_id: int, **kwargs) -> Dict:
        """Update a template"""
        db = get_db()
        try:
            template = db.query(EmailTemplate).filter(EmailTemplate.id == template_id).first()
            if not template:
                return {'status': 'not_found', 'message': 'Template not found'}
            
            for key, value in kwargs.items():
                if hasattr(template, key):
                    setattr(template, key, value)
            
            db.commit()
            return {'status': 'success', 'template': template, 'message': 'Template updated'}
        except Exception as e:
            db.rollback()
            return {'status': 'error', 'message': str(e)}
        finally:
            db.close()
    
    def delete_template(self, template_id: int) -> Dict:
        """Delete a template"""
        db = get_db()
        try:
            template = db.query(EmailTemplate).filter(EmailTemplate.id == template_id).first()
            if not template:
                return {'status': 'not_found', 'message': 'Template not found'}
            
            db.delete(template)
            db.commit()
            return {'status': 'success', 'message': 'Template deleted'}
        except Exception as e:
            db.rollback()
            return {'status': 'error', 'message': str(e)}
        finally:
            db.close()
    
    def render_template(self, template_id: int, context: Dict = None) -> Dict:
        """Render template with context variables"""
        template = self.get_template(template_id)
        if not template:
            return {'status': 'not_found', 'message': 'Template not found'}
        
        context = context or {}
        
        try:
            # Add special variables if not provided
            if 'TRACKING_PIXEL' not in context:
                context['TRACKING_PIXEL'] = '{TRACKING_PIXEL}'  # Placeholder
            if 'TRACKING_LINK' not in context:
                context['TRACKING_LINK'] = '{TRACKING_LINK}'  # Placeholder
            if 'EMAIL' not in context:
                context['EMAIL'] = '{EMAIL}'  # Placeholder
            if 'HASH' not in context:
                context['HASH'] = '{HASH}'  # Placeholder
            if 'NAME' not in context:
                context['NAME'] = '{NAME}'  # Placeholder
            
            # Render HTML - support both Jinja2 and simple string replacement
            html_body = template.body_html
            if '{' in html_body or '{{' in html_body:
                # Use Jinja2 for templates with variables
                html_template = Template(html_body)
                rendered_html = html_template.render(**context)
            else:
                # Simple string replacement for {VARIABLE} format
                rendered_html = html_body
                for key, value in context.items():
                    rendered_html = rendered_html.replace(f'{{{key}}}', str(value))
            
            # Render text
            rendered_text = None
            if template.body_text:
                if '{' in template.body_text or '{{' in template.body_text:
                    text_template = Template(template.body_text)
                    rendered_text = text_template.render(**context)
                else:
                    rendered_text = template.body_text
                    for key, value in context.items():
                        rendered_text = rendered_text.replace(f'{{{key}}}', str(value))
            
            # Render subject
            if '{' in template.subject or '{{' in template.subject:
                subject_template = Template(template.subject)
                rendered_subject = subject_template.render(**context)
            else:
                rendered_subject = template.subject
                for key, value in context.items():
                    rendered_subject = rendered_subject.replace(f'{{{key}}}', str(value))
            
            return {
                'status': 'success',
                'subject': rendered_subject,
                'body_html': rendered_html,
                'body_text': rendered_text
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def create_default_templates(self):
        """Create some default templates"""
        templates = [
            {
                'name': 'Welcome Email',
                'subject': 'Welcome to {{company_name}}!',
                'body_html': '''
                <html>
                <body>
                    <h1>Welcome {{first_name}}!</h1>
                    <p>Thank you for joining {{company_name}}. We're excited to have you on board!</p>
                    <p>Best regards,<br>The {{company_name}} Team</p>
                </body>
                </html>
                ''',
                'body_text': 'Welcome {{first_name}}! Thank you for joining {{company_name}}.'
            },
            {
                'name': 'Newsletter',
                'subject': '{{newsletter_title}} - Newsletter',
                'body_html': '''
                <html>
                <body>
                    <h1>{{newsletter_title}}</h1>
                    <p>Hello {{first_name}},</p>
                    <div>{{content}}</div>
                    <p><a href="{{unsubscribe_url}}">Unsubscribe</a></p>
                </body>
                </html>
                ''',
                'body_text': '{{newsletter_title}}\n\n{{content}}\n\nUnsubscribe: {{unsubscribe_url}}'
            },
            {
                'name': 'Promotional',
                'subject': 'Special Offer: {{offer_title}}',
                'body_html': '''
                <html>
                <body>
                    <h1>{{offer_title}}</h1>
                    <p>Hi {{first_name}},</p>
                    <p>{{offer_description}}</p>
                    <p><a href="{{offer_link}}">Claim Offer</a></p>
                </body>
                </html>
                ''',
                'body_text': '{{offer_title}}\n\n{{offer_description}}\n\nClaim Offer: {{offer_link}}'
            }
        ]
        
        results = []
        for template_data in templates:
            result = self.create_template(**template_data)
            results.append(result)
        
        return results

