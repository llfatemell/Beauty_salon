from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Line, Customer, Reservation

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

def require_auth(request: Request):
    """فقط ادمین به داشبورد دسترسی دارد"""
    if not request.session.get("admin_id"):
        return False
    return True

@router.get("/stats")
async def dashboard_stats(request: Request, db: Session = Depends(get_db)):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})

    # آمار پایه
    total_lines = db.query(Line).filter(Line.is_active == 1).count()
    total_customers = db.query(Customer).count()
    total_reservations = db.query(Reservation).count()
    confirmed_reservations = db.query(Reservation).filter(Reservation.status == 'confirmed').count()
    completed_reservations = db.query(Reservation).filter(Reservation.status == 'completed').count()
    cancelled_reservations = db.query(Reservation).filter(Reservation.status == 'cancelled').count()
    
    # درآمد کل (مجموع قیمت رزروهای تکمیل شده)
    total_revenue = db.query(func.sum(Reservation.total_price)).filter(Reservation.status == 'completed').scalar() or 0

    # محبوب‌ترین لاین (بیشترین تعداد رزرو confirmed/completed)
    popular_line_result = (
        db.query(Line.name, func.count(Reservation.id).label("reservation_count"))
        .join(Reservation, Line.id == Reservation.line_id)
        .filter(Reservation.status.in_(['confirmed', 'completed']))
        .group_by(Line.id)
        .order_by(func.count(Reservation.id).desc())
        .first()
    )
    
    popular_line_name = popular_line_result.name if popular_line_result else "هیچ رزروی ثبت نشده"
    popular_line_count = popular_line_result.reservation_count if popular_line_result else 0

    # ۵ رزرو اخیر
    recent_reservations = (
        db.query(Reservation)
        .order_by(Reservation.reservation_date.desc())
        .limit(5)
        .all()
    )
    recent_list = []
    for r in recent_reservations:
        customer = db.query(Customer).filter(Customer.id == r.customer_id).first()
        line = db.query(Line).filter(Line.id == r.line_id).first()
        recent_list.append({
            "id": r.id,
            "reservation_code": r.reservation_code,
            "customer_name": f"{customer.first_name} {customer.last_name}" if customer else "N/A",
            "line_name": line.name if line else "N/A",
            "reservation_date": r.reservation_date.isoformat(),
            "total_price": r.total_price,
            "status": r.status,
        })

    return {
        "total_lines": total_lines,
        "total_customers": total_customers,
        "total_reservations": total_reservations,
        "confirmed_reservations": confirmed_reservations,
        "completed_reservations": completed_reservations,
        "cancelled_reservations": cancelled_reservations,
        "total_revenue": round(total_revenue, 2),
        "popular_line": {
            "name": popular_line_name,
            "reservation_count": popular_line_count,
        },
        "recent_reservations": recent_list,
    }