from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, database, auth
from app.routes.auth_routes import get_current_user

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.patch("/users/{user_id}/upgrade")
def upgrade_user(
    user_id: int,
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
        from app.profile import generate_corporate_email
        corporate_email = generate_corporate_email(db, target_user.phone_number)
        new_profile = models.EmployeeProfile(
            user_id=target_user.id,
            first_name="",
            last_name="",
            corporate_email=corporate_email
        )
        db.add(new_profile)
        db.commit()
    
    return {"msg": "Роль пользователя обновлена на работник"}
