import hashlib
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Admin, Customer
from app.schemas.auth import LoginRequest, LoginResponse

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/login", response_model=LoginResponse)
async def login(body: LoginRequest, request: Request, db: Session = Depends(get_db)):
    # هش کردن رمز عبور
    pw_hash = hashlib.sha256(body.password.encode()).hexdigest()
    
    if body.role == "admin":
        user = db.query(Admin).filter(
            Admin.username == body.username,
            Admin.password_hash == pw_hash,
            Admin.is_active == 1
        ).first()
        if not user:
            return JSONResponse(
                status_code=401,
                content={"success": False, "message": "نام کاربری یا رمز عبور اشتباه است"}
            )
        request.session["admin_id"] = user.id
        request.session["role"] = "admin"
        return LoginResponse(success=True, user_id=user.id, role="admin", message="خوش آمدید")
    
    elif body.role == "customer":
        # در اینجا username همان شماره تلفن مشتری است
        user = db.query(Customer).filter(
            Customer.phone_number == body.username,
            Customer.password_hash == pw_hash,
            Customer.is_active == 1
        ).first()
        if not user:
            return JSONResponse(
                status_code=401,
                content={"success": False, "message": "شماره تلفن یا رمز عبور اشتباه است"}
            )
        request.session["customer_id"] = user.id
        request.session["role"] = "customer"
        return LoginResponse(success=True, user_id=user.id, role="customer", message="خوش آمدید")
    
    else:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": "نقش نامعتبر است"}
        )

@router.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return {"success": True, "message": "خروج از حساب با موفقیت انجام شد"}

@router.get("/me")
async def get_current_user(request: Request, db: Session = Depends(get_db)):
    admin_id = request.session.get("admin_id")
    customer_id = request.session.get("customer_id")
    if admin_id:
        admin = db.query(Admin).filter(Admin.id == admin_id).first()
        if admin:
            return {"id": admin.id, "username": admin.username, "role": "admin", "full_name": admin.full_name}
    if customer_id:
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if customer:
            return {
                "id": customer.id,
                "phone_number": customer.phone_number,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "role": "customer"
            }
    return JSONResponse(status_code=401, content={"message": "Not authenticated"})