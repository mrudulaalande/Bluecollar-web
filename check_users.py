
from backend.database import SessionLocal
from backend.models.user import User

db = SessionLocal()
users = db.query(User).all()
print("ID | Email | Role | Is Active | Is Approved")
print("-" * 50)
for u in users:
    print(f"{u.id} | {u.email} | {u.role} | {u.is_active} | {u.is_approved}")
db.close()
