"""
Segment Management Module
إدارة التقسيمات
"""

from database import get_db, Segment, SegmentMember, Contact
from typing import Dict, List
import json

class SegmentManager:
    """Manage user segments"""
    
    def create_segment(self, name: str, description: str = None, 
                      conditions: Dict = None) -> Dict:
        """Create a new segment"""
        db = get_db()
        try:
            segment = Segment(
                name=name,
                description=description,
                conditions=json.dumps(conditions) if conditions else None
            )
            db.add(segment)
            db.commit()
            db.refresh(segment)
            return {'status': 'success', 'segment': segment}
        except Exception as e:
            db.rollback()
            return {'status': 'error', 'message': str(e)}
        finally:
            db.close()
    
    def get_segment(self, segment_id: int) -> Segment:
        """Get segment by ID"""
        db = get_db()
        try:
            return db.query(Segment).filter(Segment.id == segment_id).first()
        finally:
            db.close()
    
    def list_segments(self) -> List[Segment]:
        """List all segments"""
        db = get_db()
        try:
            return db.query(Segment).all()
        finally:
            db.close()
    
    def add_to_segment(self, segment_id: int, contact_id: int) -> Dict:
        """Add contact to segment"""
        db = get_db()
        try:
            # Check if already in segment
            existing = db.query(SegmentMember).filter(
                SegmentMember.segment_id == segment_id,
                SegmentMember.contact_id == contact_id
            ).first()
            
            if existing:
                return {'status': 'exists', 'message': 'Contact already in segment'}
            
            member = SegmentMember(segment_id=segment_id, contact_id=contact_id)
            db.add(member)
            db.commit()
            return {'status': 'success', 'message': 'Contact added to segment'}
        except Exception as e:
            db.rollback()
            return {'status': 'error', 'message': str(e)}
        finally:
            db.close()
    
    def get_segment_contacts(self, segment_id: int) -> List[Contact]:
        """Get all contacts in a segment"""
        db = get_db()
        try:
            members = db.query(SegmentMember).filter(
                SegmentMember.segment_id == segment_id
            ).all()
            return [member.contact for member in members]
        finally:
            db.close()
    
    def apply_segment_conditions(self, segment_id: int) -> List[Contact]:
        """Apply segment conditions and get matching contacts"""
        db = get_db()
        try:
            segment = db.query(Segment).filter(Segment.id == segment_id).first()
            if not segment or not segment.conditions:
                return []
            
            conditions = json.loads(segment.conditions)
            query = db.query(Contact)
            
            # Apply filters based on conditions
            if 'status' in conditions:
                query = query.filter(Contact.status == conditions['status'])
            if 'tags' in conditions:
                # Filter by tags (simplified)
                pass
            
            return query.all()
        finally:
            db.close()
    
    def delete_segment(self, segment_id: int) -> Dict:
        """Delete a segment"""
        db = get_db()
        try:
            segment = db.query(Segment).filter(Segment.id == segment_id).first()
            if not segment:
                return {'status': 'not_found', 'message': 'Segment not found'}
            
            db.delete(segment)
            db.commit()
            return {'status': 'success', 'message': 'Segment deleted'}
        except Exception as e:
            db.rollback()
            return {'status': 'error', 'message': str(e)}
        finally:
            db.close()

