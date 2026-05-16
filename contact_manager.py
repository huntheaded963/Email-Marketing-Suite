"""
Contact and list management module
"""
from database import get_db, Contact, ContactList, ContactListMember
from typing import List, Dict, Optional
from sqlalchemy import or_
import json

class ContactManager:
    """Manage contacts and email lists"""
    
    def add_contact(self, email: str, first_name: str = None, 
                   last_name: str = None, phone: str = None,
                   tags: List[str] = None) -> Dict:
        """Add a new contact"""
        db = get_db()
        try:
            # Check if contact exists
            existing = db.query(Contact).filter(Contact.email == email).first()
            if existing:
                return {'status': 'exists', 'contact': existing, 'message': 'Contact already exists'}
            
            contact = Contact(
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                tags=json.dumps(tags) if tags else None,
                status='active'
            )
            db.add(contact)
            db.commit()
            db.refresh(contact)
            
            return {'status': 'success', 'contact': contact, 'message': 'Contact added successfully'}
        except Exception as e:
            db.rollback()
            return {'status': 'error', 'message': str(e)}
        finally:
            db.close()
    
    def get_contact(self, email: str = None, contact_id: int = None) -> Optional[Contact]:
        """Get contact by email or ID"""
        db = get_db()
        try:
            if email:
                return db.query(Contact).filter(Contact.email == email).first()
            elif contact_id:
                return db.query(Contact).filter(Contact.id == contact_id).first()
            return None
        finally:
            db.close()
    
    def list_contacts(self, status: str = None, limit: int = 100, offset: int = 0) -> List[Contact]:
        """List all contacts with optional filtering"""
        db = get_db()
        try:
            query = db.query(Contact)
            if status:
                query = query.filter(Contact.status == status)
            return query.limit(limit).offset(offset).all()
        finally:
            db.close()
    
    def update_contact(self, email: str, **kwargs) -> Dict:
        """Update contact information"""
        db = get_db()
        try:
            contact = db.query(Contact).filter(Contact.email == email).first()
            if not contact:
                return {'status': 'not_found', 'message': 'Contact not found'}
            
            for key, value in kwargs.items():
                if hasattr(contact, key):
                    if key == 'tags' and isinstance(value, list):
                        setattr(contact, key, json.dumps(value))
                    else:
                        setattr(contact, key, value)
            
            db.commit()
            return {'status': 'success', 'contact': contact, 'message': 'Contact updated'}
        except Exception as e:
            db.rollback()
            return {'status': 'error', 'message': str(e)}
        finally:
            db.close()
    
    def delete_contact(self, email: str) -> Dict:
        """Delete a contact"""
        db = get_db()
        try:
            contact = db.query(Contact).filter(Contact.email == email).first()
            if not contact:
                return {'status': 'not_found', 'message': 'Contact not found'}
            
            db.delete(contact)
            db.commit()
            return {'status': 'success', 'message': 'Contact deleted'}
        except Exception as e:
            db.rollback()
            return {'status': 'error', 'message': str(e)}
        finally:
            db.close()
    
    def unsubscribe(self, email: str) -> Dict:
        """Unsubscribe a contact"""
        return self.update_contact(email, status='unsubscribed')
    
    def create_list(self, name: str, description: str = None) -> Dict:
        """Create a new contact list"""
        db = get_db()
        try:
            contact_list = ContactList(name=name, description=description)
            db.add(contact_list)
            db.commit()
            db.refresh(contact_list)
            return {'status': 'success', 'list': contact_list, 'message': 'List created'}
        except Exception as e:
            db.rollback()
            return {'status': 'error', 'message': str(e)}
        finally:
            db.close()
    
    def add_to_list(self, list_id: int, contact_id: int) -> Dict:
        """Add contact to a list"""
        db = get_db()
        try:
            # Check if already in list
            existing = db.query(ContactListMember).filter(
                ContactListMember.list_id == list_id,
                ContactListMember.contact_id == contact_id
            ).first()
            
            if existing:
                return {'status': 'exists', 'message': 'Contact already in list'}
            
            member = ContactListMember(list_id=list_id, contact_id=contact_id)
            db.add(member)
            db.commit()
            return {'status': 'success', 'message': 'Contact added to list'}
        except Exception as e:
            db.rollback()
            return {'status': 'error', 'message': str(e)}
        finally:
            db.close()
    
    def get_list_contacts(self, list_id: int) -> List[Contact]:
        """Get all contacts in a list"""
        db = get_db()
        try:
            members = db.query(ContactListMember).filter(
                ContactListMember.list_id == list_id
            ).all()
            return [member.contact for member in members]
        finally:
            db.close()
    
    def get_all_lists(self) -> List[ContactList]:
        """Get all contact lists"""
        db = get_db()
        try:
            return db.query(ContactList).all()
        finally:
            db.close()
    
    def import_contacts(self, contacts: List[Dict]) -> Dict:
        """Import multiple contacts"""
        results = {'success': 0, 'failed': 0, 'exists': 0, 'errors': []}
        
        for contact_data in contacts:
            result = self.add_contact(**contact_data)
            if result['status'] == 'success':
                results['success'] += 1
            elif result['status'] == 'exists':
                results['exists'] += 1
            else:
                results['failed'] += 1
                results['errors'].append(result.get('message', 'Unknown error'))
        
        return results

