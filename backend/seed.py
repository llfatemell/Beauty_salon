"""Seed script — populates the beauty salon database with sample data."""
import hashlib
from datetime import datetime, timedelta
from app.database import SessionLocal, engine, Base
from app.models import Admin, Customer, Line, WorkSchedule, Reservation, Holiday

# ایجاد جداول در صورت عدم وجود
Base.metadata.create_all(bind=engine)
db = SessionLocal()

# اگر قبلاً ادمینی وجود دارد، از seeding صرف نظر کن
if db.query(Admin).count() > 0:
    print("Database already seeded. Skipping.")
    db.close()
    exit(0)

# ==================== 1. ادمین ====================
admin = Admin(
    username="admin",
    password_hash=hashlib.sha256("admin123".encode()).hexdigest(),
    full_name="مدیر اصلی",
    is_active=1
)
db.add(admin)

# ==================== 2. لاین‌ها (خدمات) ====================
lines_data = [
    {"name": "ناخن", "duration_minutes": 90, "price": 350000, "is_active": 1},
    {"name": "مو", "duration_minutes": 60, "price": 400000, "is_active": 1},
    {"name": "میکاپ", "duration_minutes": 45, "price": 500000, "is_active": 1},
    {"name": "ماساژ", "duration_minutes": 120, "price": 550000, "is_active": 1},
    {"name": "ابرو", "duration_minutes": 30, "price": 150000, "is_active": 1},
]
lines = []
for data in lines_data:
    line = Line(**data)
    db.add(line)
    lines.append(line)
db.flush()

# ==================== 3. مشتریان ====================
customers_data = [
    {
        "first_name": "علی",
        "last_name": "محمدی",
        "phone_number": "09121112222",
        "password_hash": hashlib.sha256("123456".encode()).hexdigest(),
        "email": "ali@example.com",
        "phone_verified": 1,
        "birth_date": "1990-01-01",
        "gender": "male",
        "address": "تهران، خیابان آزادی",
        "notes": "مشتری وفادار",
        "is_active": 1
    },
    {
        "first_name": "مریم",
        "last_name": "کریمی",
        "phone_number": "09351234567",
        "password_hash": hashlib.sha256("123456".encode()).hexdigest(),
        "email": "maryam@example.com",
        "phone_verified": 1,
        "birth_date": "1985-05-12",
        "gender": "female",
        "address": "اصفهان، خیابان نقش جهان",
        "notes": "آلرژی به عطر",
        "is_active": 1
    },
    {
        "first_name": "رضا",
        "last_name": "نوری",
        "phone_number": "09018887777",
        "password_hash": hashlib.sha256("123456".encode()).hexdigest(),
        "email": "reza@example.com",
        "phone_verified": 0,
        "birth_date": "1992-08-20",
        "gender": "male",
        "address": "شیراز، خیابان زند",
        "notes": None,
        "is_active": 1
    },
    {
        "first_name": "سارا",
        "last_name": "حسینی",
        "phone_number": "09103334444",
        "password_hash": hashlib.sha256("123456".encode()).hexdigest(),
        "email": "sara@example.com",
        "phone_verified": 1,
        "birth_date": "1988-11-03",
        "gender": "female",
        "address": "مشهد، خیابان امام رضا",
        "notes": "درخواست خدمات ویژه",
        "is_active": 1
    },
    {
        "first_name": "احمد",
        "last_name": "رضایی",
        "phone_number": "09362223333",
        "password_hash": hashlib.sha256("123456".encode()).hexdigest(),
        "email": "ahmad@example.com",
        "phone_verified": 1,
        "birth_date": "1975-12-25",
        "gender": "male",
        "address": "تبریز، خیابان امام خمینی",
        "notes": "عضویت در طرح تخفیف",
        "is_active": 1
    }
]
customers = []
for data in customers_data:
    cust = Customer(**data)
    db.add(cust)
    customers.append(cust)
db.flush()

# ==================== 4. ساعات کاری (work_schedules) ====================
# weekday: 0=دوشنبه, 1=سه‌شنبه, 2=چهارشنبه, 3=پنج‌شنبه, 4=جمعه, 5=شنبه, 6=یکشنبه
schedules_data = [
    # ناخن (lines[0])
    (lines[0].id, 0, "09:00", "18:00"),
    (lines[0].id, 1, "09:00", "18:00"),
    (lines[0].id, 2, "09:00", "18:00"),
    (lines[0].id, 3, "09:00", "14:00"),
    (lines[0].id, 4, "10:00", "16:00"),
    (lines[0].id, 5, "09:00", "18:00"),
    # مو (lines[1])
    (lines[1].id, 0, "10:00", "19:00"),
    (lines[1].id, 1, "10:00", "19:00"),
    (lines[1].id, 2, "10:00", "19:00"),
    (lines[1].id, 3, "10:00", "15:00"),
    (lines[1].id, 5, "10:00", "19:00"),
    # میکاپ (lines[2])
    (lines[2].id, 1, "11:00", "20:00"),
    (lines[2].id, 2, "11:00", "20:00"),
    (lines[2].id, 4, "09:00", "14:00"),
    (lines[2].id, 5, "11:00", "20:00"),
    # ماساژ (lines[3])
    (lines[3].id, 1, "12:00", "22:00"),
    (lines[3].id, 2, "12:00", "22:00"),
    (lines[3].id, 4, "10:00", "20:00"),
    (lines[3].id, 6, "12:00", "22:00"),
    # ابرو (lines[4])
    (lines[4].id, 0, "08:00", "17:00"),
    (lines[4].id, 3, "08:00", "13:00"),
    (lines[4].id, 6, "08:00", "17:00"),
]
for line_id, weekday, start, end in schedules_data:
    ws = WorkSchedule(line_id=line_id, weekday=weekday, start_time=start, end_time=end)
    db.add(ws)

# ==================== 5. رزروها ====================
# زمان مبنا (فردا ساعت 10 صبح)
base_date = datetime.utcnow().replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=1)

reservations_data = [
    {
        "reservation_code": "RES-001",
        "customer_id": customers[0].id,
        "line_id": lines[0].id,
        "reservation_date": base_date,
        "duration_minutes": lines[0].duration_minutes,
        "total_price": lines[0].price,
        "status": "confirmed"
    },
    {
        "reservation_code": "RES-002",
        "customer_id": customers[1].id,
        "line_id": lines[1].id,
        "reservation_date": base_date + timedelta(hours=2),
        "duration_minutes": lines[1].duration_minutes,
        "total_price": lines[1].price,
        "status": "confirmed"
    },
    {
        "reservation_code": "RES-003",
        "customer_id": customers[2].id,
        "line_id": lines[4].id,
        "reservation_date": base_date + timedelta(days=1, hours=11),
        "duration_minutes": lines[4].duration_minutes,
        "total_price": lines[4].price,
        "status": "completed"
    },
    {
        "reservation_code": "RES-004",
        "customer_id": customers[3].id,
        "line_id": lines[3].id,
        "reservation_date": base_date + timedelta(days=1, hours=16),
        "duration_minutes": lines[3].duration_minutes,
        "total_price": lines[3].price,
        "status": "confirmed"
    },
    {
        "reservation_code": "RES-005",
        "customer_id": customers[0].id,
        "line_id": lines[2].id,
        "reservation_date": base_date + timedelta(days=2, hours=9, minutes=45),
        "duration_minutes": lines[2].duration_minutes,
        "total_price": lines[2].price,
        "status": "cancelled"
    },
    {
        "reservation_code": "RES-006",
        "customer_id": customers[1].id,
        "line_id": lines[0].id,
        "reservation_date": base_date + timedelta(days=3, hours=12),
        "duration_minutes": lines[0].duration_minutes,
        "total_price": lines[0].price,
        "status": "confirmed"
    }
]
for data in reservations_data:
    res = Reservation(**data)
    db.add(res)

# ==================== 6. تعطیلات ====================
holidays_data = [
    {"holiday_date": "2025-04-01", "description": "تعطیلات نوروزی"},
    {"holiday_date": "2025-04-02", "description": "تعطیلات نوروزی"},
    {"holiday_date": "2025-09-17", "description": "تاسوعای حسینی"},
]
for data in holidays_data:
    h = Holiday(**data)
    db.add(h)

# ذخیره نهایی
db.commit()
db.close()
print("Salon database seeded successfully!")