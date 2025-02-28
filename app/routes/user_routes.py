from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models
from app.database import get_db
from pydantic import BaseModel

router = APIRouter()

class UpgradeUserRequest(BaseModel):
    first_name: str
    last_name: str

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

    from app.models import EmployeeProfile
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

@router.patch("/users/{user_id}/upgrade")
async def upgrade_user(
    user_id: int,
    upgrade_data: UpgradeUserRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.system_role != "admin":
        raise HTTPException(status_code=403, detail="Доступ запрещён")
    
    target_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    if target_user.system_role != "guest":
        raise HTTPException(status_code=400, detail="Можно обновить только роль гостя")
    
    target_user.system_role = "employee"
    db.commit()
    
    if not target_user.profile:
        full_name = f"{upgrade_data.first_name} {upgrade_data.last_name}"
        corporate_email = generate_corporate_email(db, full_name)
        new_profile = models.EmployeeProfile(
            user_id=target_user.id,
            first_name=upgrade_data.first_name,
            last_name=upgrade_data.last_name,
            corporate_email=corporate_email
        )
        db.add(new_profile)
        db.commit()
    
    return {"msg": "Роль пользователя обновлена на работник"}

@router.get("/users")
async def get_all_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.system_role != "admin":
        raise HTTPException(status_code=403, detail="Доступ запрещён")
    
    users = db.query(models.User).all()
    return users

@router.get("/users/guests")
async def get_guest_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.system_role != "admin":
        raise HTTPException(status_code=403, detail="Доступ запрещён")
    
    guest_users = db.query(models.User).filter(models.User.system_role == "guest").all()
    return guest_users
