from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password, create_access_token
from app.models.User import User


class UserService:
    @staticmethod
    def create_user(username: str, password: str, db: Session):
        user = db.query(User).filter(User.username == username).first()
        if user:
            return None

        hashed_password = hash_password(password)
        new_user = User(username=username, hashed_password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def authenticate_user(username: str, password: str, db: Session):
        user = db.query(User).filter(User.username == username).first()
        if not user or not verify_password(password, user.hashed_password):
            return None  # Authentication failed
        return user

    @staticmethod
    def generate_token(user: User):
        return create_access_token(data={"sub": user.username})