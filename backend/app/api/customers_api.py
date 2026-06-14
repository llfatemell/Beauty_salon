from fastapi import APIRouter, Request, Depends, Query, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse

router = APIRouter(prefix="/api/customers", tags=["Customers"])

def require_auth(request: Request):
    """فقط ادمین اجازه دسترسی به این API را دارد"""
    if not request.session.get("admin_id"):
        return False
    return True

@router.get("")
async def list_customers(
    request: Request,
    sort: str = Query("id", description="فیلد مرتب‌سازی: id, first_name, last_name, phone_number, total_visits, register_date"),
    order: str = Query("asc", description="asc یا desc"),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    search: str = Query("", description="جستجو در نام یا شماره تلفن"),
    db: Session = Depends(get_db),
):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})

    # نقشه فیلدهای قابل مرتب‌سازی
    sort_map = {
        "id": Customer.id,
        "first_name": Customer.first_name,
        "last_name": Customer.last_name,
        "phone_number": Customer.phone_number,
        "total_visits": Customer.total_visits,
        "register_date": Customer.register_date,
    }
    sort_column = sort_map.get(sort, Customer.id)
    if order.lower() == "desc":
        sort_column = sort_column.desc()
    else:
        sort_column = sort_column.asc()

    # اعمال فیلتر جستجو
    query = db.query(Customer)
    if search:
        query = query.filter(
            (Customer.first_name.contains(search)) |
            (Customer.last_name.contains(search)) |
            (Customer.phone_number.contains(search))
        )

    total = query.count()
    customers = query.order_by(sort_column).offset((page - 1) * per_page).limit(per_page).all()

    # تبدیل به response model
    return {
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page if total > 0 else 1,
        "customers": [
            CustomerResponse(
                id=c.id,
                first_name=c.first_name,
                last_name=c.last_name,
                phone_number=c.phone_number,
                email=c.email,
                birth_date=c.birth_date,
                gender=c.gender,
                address=c.address,
                notes=c.notes,
                register_date=c.register_date,
                total_visits=c.total_visits,
                phone_verified=c.phone_verified,
                is_active=c.is_active,
                last_login=c.last_login,
            )
            for c in customers
        ],
    }

@router.get("/{customer_id}")
async def get_customer(
    request: Request, customer_id: int, db: Session = Depends(get_db)
):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})
    c = db.query(Customer).filter(Customer.id == customer_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Customer not found")
    return CustomerResponse(
        id=c.id,
        first_name=c.first_name,
        last_name=c.last_name,
        phone_number=c.phone_number,
        email=c.email,
        birth_date=c.birth_date,
        gender=c.gender,
        address=c.address,
        notes=c.notes,
        register_date=c.register_date,
        total_visits=c.total_visits,
        phone_verified=c.phone_verified,
        is_active=c.is_active,
        last_login=c.last_login,
    )

@router.post("", status_code=201)
async def create_customer(
    request: Request, body: CustomerCreate, db: Session = Depends(get_db)
):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})
    
    # بررسی یکتایی شماره تلفن
    existing = db.query(Customer).filter(Customer.phone_number == body.phone_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    # هش کردن رمز عبور (در صورت وجود) - در مدل CustomerCreate حتماً password وجود دارد
    import hashlib
    hashed_password = hashlib.sha256(body.password.encode()).hexdigest() if body.password else ""
    
    # ایجاد مشتری جدید (فیلدهای اضافی را در صورت نیاز از body بگیر)
    new_customer = Customer(
        first_name=body.first_name,
        last_name=body.last_name,
        phone_number=body.phone_number,
        password_hash=hashed_password,
        email=body.email,
        birth_date=body.birth_date,
        gender=body.gender,
        address=body.address,
        notes=body.notes,
        phone_verified=body.phone_verified if body.phone_verified is not None else 0,
        is_active=body.is_active if body.is_active is not None else 1,
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return CustomerResponse(
        id=new_customer.id,
        first_name=new_customer.first_name,
        last_name=new_customer.last_name,
        phone_number=new_customer.phone_number,
        email=new_customer.email,
        birth_date=new_customer.birth_date,
        gender=new_customer.gender,
        address=new_customer.address,
        notes=new_customer.notes,
        register_date=new_customer.register_date,
        total_visits=new_customer.total_visits,
        phone_verified=new_customer.phone_verified,
        is_active=new_customer.is_active,
        last_login=new_customer.last_login,
    )

@router.put("/{customer_id}")
async def update_customer(
    request: Request, customer_id: int, body: CustomerCreate, db: Session = Depends(get_db)
):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})
    c = db.query(Customer).filter(Customer.id == customer_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # بررسی یکتایی شماره تلفن (اگر تغییر کرده)
    if body.phone_number != c.phone_number:
        existing = db.query(Customer).filter(Customer.phone_number == body.phone_number).first()
        if existing:
            raise HTTPException(status_code=400, detail="Phone number already taken")
    
    # به‌روزرسانی فیلدها
    c.first_name = body.first_name
    c.last_name = body.last_name
    c.phone_number = body.phone_number
    c.email = body.email
    c.birth_date = body.birth_date
    c.gender = body.gender
    c.address = body.address
    c.notes = body.notes
    c.phone_verified = body.phone_verified if body.phone_verified is not None else c.phone_verified
    c.is_active = body.is_active if body.is_active is not None else c.is_active
    
    # اگر رمز عبور جدید داده شده، هش و ذخیره کن
    if body.password:
        import hashlib
        c.password_hash = hashlib.sha256(body.password.encode()).hexdigest()
    
    db.commit()
    db.refresh(c)
    return CustomerResponse(
        id=c.id,
        first_name=c.first_name,
        last_name=c.last_name,
        phone_number=c.phone_number,
        email=c.email,
        birth_date=c.birth_date,
        gender=c.gender,
        address=c.address,
        notes=c.notes,
        register_date=c.register_date,
        total_visits=c.total_visits,
        phone_verified=c.phone_verified,
        is_active=c.is_active,
        last_login=c.last_login,
    )

@router.patch("/{customer_id}")
async def patch_customer(
    request: Request, customer_id: int, body: CustomerUpdate, db: Session = Depends(get_db)
):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})
    c = db.query(Customer).filter(Customer.id == customer_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # به‌روزرسانی فقط فیلدهای ارسال شده
    update_data = body.model_dump(exclude_unset=True)
    if "phone_number" in update_data and update_data["phone_number"] != c.phone_number:
        existing = db.query(Customer).filter(Customer.phone_number == update_data["phone_number"]).first()
        if existing:
            raise HTTPException(status_code=400, detail="Phone number already taken")
    
    for key, value in update_data.items():
        if key == "password" and value:
            import hashlib
            setattr(c, "password_hash", hashlib.sha256(value.encode()).hexdigest())
        elif key != "password":
            setattr(c, key, value)
    
    db.commit()
    db.refresh(c)
    return CustomerResponse(
        id=c.id,
        first_name=c.first_name,
        last_name=c.last_name,
        phone_number=c.phone_number,
        email=c.email,
        birth_date=c.birth_date,
        gender=c.gender,
        address=c.address,
        notes=c.notes,
        register_date=c.register_date,
        total_visits=c.total_visits,
        phone_verified=c.phone_verified,
        is_active=c.is_active,
        last_login=c.last_login,
    )

@router.delete("/{customer_id}")
async def delete_customer(
    request: Request, customer_id: int, db: Session = Depends(get_db)
):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})
    c = db.query(Customer).filter(Customer.id == customer_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(c)
    db.commit()
    return {"message": "Customer deleted"}