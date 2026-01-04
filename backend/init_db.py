"""
Database initialization script
Creates tables and seeds initial admin user
"""
from backend.database import engine, Base, SessionLocal
from backend.models.user import User, UserRole
from backend.models.worker import WorkerProfile
from backend.models.booking import Booking
from backend.models.review import Review
from backend.models.payment import Payment
from backend.core.security import get_password_hash


def init_db():
    """Initialize database with tables and seed data"""
    
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created successfully")
    
    # Create session
    db = SessionLocal()
    
    try:
        # Check if admin already exists
        admin = db.query(User).filter(User.email == "admin@bluecollar.com").first()
        
        if not admin:
            print("\nCreating default admin user...")
            admin = User(
                email="admin@bluecollar.com",
                hashed_password=get_password_hash("Admin@123"),
                full_name="System Administrator",
                role=UserRole.ADMIN,
                phone="+1234567890",
                is_active=True,
                is_approved=True
            )
            db.add(admin)
            db.commit()
            print("✓ Admin user created")
            print("  Email: admin@bluecollar.com")
            print("  Password: Admin@123")
            print("  ⚠️  CHANGE THIS PASSWORD IN PRODUCTION!")
        else:
            print("\n✓ Admin user already exists")
        
        print("\n✅ Database initialization complete!")
        
    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
