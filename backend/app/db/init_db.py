from sqlalchemy.orm import Session

from app.core.database import engine, Base
from app.core.security import get_password_hash
from app.models import User
from app.models.user import UserRole


def init_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")


def create_default_user(db: Session):
    # Check if admin user exists
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        admin_user = User(
            username="admin",
            email="admin@facescan.local",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        print("Default admin user created: username=admin, password=admin123")

    # Check if guard user exists
    guard = db.query(User).filter(User.username == "guard").first()
    if not guard:
        guard_user = User(
            username="guard",
            email="guard@facescan.local",
            hashed_password=get_password_hash("guard123"),
            role=UserRole.GUARD,
            is_active=True
        )
        db.add(guard_user)
        db.commit()
        print("Default guard user created: username=guard, password=guard123")


if __name__ == "__main__":
    from app.core.database import SessionLocal

    init_db()

    db = SessionLocal()
    try:
        create_default_user(db)
    finally:
        db.close()

    print("Database initialization completed")
