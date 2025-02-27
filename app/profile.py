import re
from sqlalchemy.orm import Session
from app.models import EmployeeProfile

def transliterate(text: str) -> str:
    mapping = {
        'А': 'A', 'а': 'a',
        'Б': 'B', 'б': 'b',
        'В': 'V', 'в': 'v',
        'Г': 'G', 'г': 'g',
        'Д': 'D', 'д': 'd',
        'Е': 'E', 'е': 'e',
        'Ё': 'Yo', 'ё': 'yo',
        'Ж': 'Zh', 'ж': 'zh',
        'З': 'Z', 'з': 'z',
        'И': 'I', 'и': 'i',
        'Й': 'Y', 'й': 'y',
        'К': 'K', 'к': 'k',
        'Л': 'L', 'л': 'l',
        'М': 'M', 'м': 'm',
        'Н': 'N', 'н': 'n',
        'О': 'O', 'о': 'o',
        'П': 'P', 'п': 'p',
        'Р': 'R', 'р': 'r',
        'С': 'S', 'с': 's',
        'Т': 'T', 'т': 't',
        'У': 'U', 'у': 'u',
        'Ф': 'F', 'ф': 'f',
        'Х': 'Kh', 'х': 'kh',
        'Ц': 'Ts', 'ц': 'ts',
        'Ч': 'Ch', 'ч': 'ch',
        'Ш': 'Sh', 'ш': 'sh',
        'Щ': 'Shch', 'щ': 'shch',
        'Ъ': '', 'ъ': '',
        'Ы': 'Y', 'ы': 'y',
        'Ь': '', 'ь': '',
        'Э': 'E', 'э': 'e',
        'Ю': 'Yu', 'ю': 'yu',
        'Я': 'Ya', 'я': 'ya',
    }
    return ''.join(mapping.get(char, char) for char in text)

def generate_corporate_email(db: Session, full_name: str) -> str:
    name_parts = full_name.split()
    if len(name_parts) < 2:
        raise ValueError("Необходимо имя и фамилия")
    
    transliterated_first_name = transliterate(name_parts[0])
    transliterated_last_name = transliterate(name_parts[1])
    
    first_initial = transliterated_first_name[0].lower()
    last_name = transliterated_last_name.lower()
    
    domain = "cyber-ed.ru"
    base_email = f"{first_initial}.{last_name}"
    candidate_email = f"{base_email}@{domain}"

    existing_profile = db.query(EmployeeProfile).filter(
        EmployeeProfile.corporate_email == candidate_email
    ).first()
    
    if not existing_profile:
        return candidate_email
    
    suffix = 1
    while True:
        candidate_email_with_suffix = f"{base_email}{suffix}@{domain}"
        if not db.query(EmployeeProfile).filter(
            EmployeeProfile.corporate_email == candidate_email_with_suffix
        ).first():
            return candidate_email_with_suffix
        suffix += 1
