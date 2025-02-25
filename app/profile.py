import re
from sqlalchemy.orm import Session
from app.models import EmployeeProfile

def generate_corporate_email(db: Session, full_name: str) -> str:
    name_parts = full_name.split()
    if len(name_parts) < 2:
        raise ValueError("Необходимо имя и фамилия")
    
    first_initial = name_parts[0][0].lower()
    last_name = name_parts[1].lower() 
    domain = "cyber-ed.ru"
    base_email = f"{first_initial}.{last_name}"
    candidate_email = f"{base_email}@{domain}"

    existing_profile = db.query(EmployeeProfile).filter(EmployeeProfile.corporate_email == candidate_email).first()
    if not existing_profile:
        return candidate_email
    
    suffix = 1
    while True:
        candidate_email_with_suffix = f"{base_email}{suffix}@{domain}"
        if not db.query(EmployeeProfile).filter(EmployeeProfile.corporate_email == candidate_email_with_suffix).first():
            return candidate_email_with_suffix
        suffix += 1
