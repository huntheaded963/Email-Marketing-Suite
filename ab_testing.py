"""
A/B Testing Tool for Email Marketing
اختبار A/B للحملات الإلكترونية
"""

from database import get_db, Campaign
from typing import Dict, List
import random

class ABTesting:
    """A/B Testing for email campaigns"""
    
    def create_ab_test(self, campaign_a_id: int, campaign_b_id: int, 
                      split_percentage: float = 50.0) -> Dict:
        """Create A/B test between two campaigns"""
        db = get_db()
        try:
            # Get campaigns
            campaign_a = db.query(Campaign).filter(Campaign.id == campaign_a_id).first()
            campaign_b = db.query(Campaign).filter(Campaign.id == campaign_b_id).first()
            
            if not campaign_a or not campaign_b:
                return {'status': 'error', 'message': 'Campaigns not found'}
            
            # Store A/B test configuration
            ab_test = {
                'campaign_a_id': campaign_a_id,
                'campaign_b_id': campaign_b_id,
                'split_percentage': split_percentage,
                'status': 'active'
            }
            
            return {'status': 'success', 'ab_test': ab_test}
        finally:
            db.close()
    
    def split_recipients(self, total_recipients: int, split_percentage: float = 50.0) -> Dict:
        """Split recipients for A/B testing"""
        group_a_count = int(total_recipients * (split_percentage / 100))
        group_b_count = total_recipients - group_a_count
        
        return {
            'group_a': group_a_count,
            'group_b': group_b_count,
            'total': total_recipients
        }
    
    def get_winner(self, campaign_a_stats: Dict, campaign_b_stats: Dict) -> Dict:
        """Determine A/B test winner"""
        a_open_rate = campaign_a_stats.get('open_rate', 0)
        b_open_rate = campaign_b_stats.get('open_rate', 0)
        
        a_click_rate = campaign_a_stats.get('click_rate', 0)
        b_click_rate = campaign_b_stats.get('click_rate', 0)
        
        # Calculate winner based on open rate and click rate
        a_score = (a_open_rate * 0.6) + (a_click_rate * 0.4)
        b_score = (b_open_rate * 0.6) + (b_click_rate * 0.4)
        
        if a_score > b_score:
            winner = 'A'
            improvement = ((a_score - b_score) / b_score) * 100 if b_score > 0 else 0
        elif b_score > a_score:
            winner = 'B'
            improvement = ((b_score - a_score) / a_score) * 100 if a_score > 0 else 0
        else:
            winner = 'Tie'
            improvement = 0
        
        return {
            'winner': winner,
            'improvement': round(improvement, 2),
            'campaign_a_score': round(a_score, 2),
            'campaign_b_score': round(b_score, 2)
        }

