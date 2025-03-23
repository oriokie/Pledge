import random
import string
from sqlalchemy.orm import Session
from app.models.member import Member

def generate_unique_code(db: Session) -> str:
    """Generate a unique 6-digit code for a member"""
    while True:
        # Generate a random 6-digit code
        code = ''.join(random.choices(string.digits, k=6))
        
        # Check if the code already exists
        if not db.query(Member).filter(Member.unique_code == code).first():
            return code 