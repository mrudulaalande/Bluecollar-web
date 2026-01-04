"""
Script to seed test data for testing the application
Creates a test client and a test worker
"""
from backend.database import SessionLocal, engine, Base
from backend.models.user import User, UserRole
from backend.models.worker import WorkerProfile, AvailabilityType
from backend.core.security import get_password_hash
import datetime

def seed_test_data():
    print("Seeding test data...")
    db = SessionLocal()
    
    try:
        # 1. Create Test Client
        client = db.query(User).filter(User.email == "client@test.com").first()
        if not client:
            print("Creating test client...")
            client = User(
                email="client@test.com",
                hashed_password=get_password_hash("BlueCollar#Client#99"),
                full_name="John Test Client",
                role=UserRole.CLIENT,
                phone="9876543210",
                is_active=True,
                is_approved=True
            )
            db.add(client)
            db.commit()
            print("✓ Test client created: client@test.com / BlueCollar#Client#99")
        else:
            print("Updating test client password...")
            client.hashed_password = get_password_hash("BlueCollar#Client#99")
            db.commit()
            print("✓ Test client updated: client@test.com / BlueCollar#Client#99")

        # 2. Create Test Worker User
        worker_user = db.query(User).filter(User.email == "worker@test.com").first()
        if not worker_user:
            print("Creating test worker...")
            worker_user = User(
                email="worker@test.com",
                hashed_password=get_password_hash("BlueCollar#Worker#88"),
                full_name="Bob Skilled Worker",
                role=UserRole.WORKER,
                phone="9988776655",
                is_active=True,
                is_approved=True # Auto-approve for testing
            )
            db.add(worker_user)
            db.commit()
            db.refresh(worker_user)
            print("✓ Test worker user created: worker@test.com / BlueCollar#Worker#88")
        else:
            print("Updating test worker password...")
            worker_user.hashed_password = get_password_hash("BlueCollar#Worker#88")
            db.commit()
            print("✓ Test worker updated: worker@test.com / BlueCollar#Worker#88")

        # 3. Create Worker Profile
        profile = db.query(WorkerProfile).filter(WorkerProfile.user_id == worker_user.id).first()
        if not profile:
            print("Creating worker profile...")
            profile = WorkerProfile(
                user_id=worker_user.id,
                skills="Plumber, Electrician, Repair",
                experience_years=5,
                location="Mumbai",
                pincode="400001",
                availability=AvailabilityType.FULL_TIME,
                price_per_hour=450.0,
                bio="Expert plumber and electrician with 5 years of experience in residential repairs.",
                is_available=1,
                rating=4.5,
                total_reviews=10
            )
            db.add(profile)
            db.commit()
            print("✓ Test worker profile created: worker@test.com / password123")
        # 4. Create Admin User
        admin = db.query(User).filter(User.email == "admin@bluecollar.com").first()
        if not admin:
            print("Creating admin user...")
            admin = User(
                email="admin@bluecollar.com",
                hashed_password=get_password_hash("BlueCollar#Admin#77"),
                full_name="Platform Administrator",
                role=UserRole.ADMIN,
                phone="1234567890",
                is_active=True,
                is_approved=True
            )
            db.add(admin)
            db.commit()
            print("✓ Admin user created: admin@bluecollar.com / BlueCollar#Admin#77")
        else:
            print("Updating admin password...")
            admin.hashed_password = get_password_hash("BlueCollar#Admin#77")
            db.commit()
            print("✓ Admin password updated")

        print("\n✅ Test data seeding complete!")
        print("\nCredentials:")
        print("  Client: client@test.com / BlueCollar#Client#99")
        print("  Worker: worker@test.com / BlueCollar#Worker#88")
        print("  Admin: admin@bluecollar.com / BlueCollar#Admin#77")

    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_test_data()
