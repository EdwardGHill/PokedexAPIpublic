from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from connection import Base
from pydantic import BaseModel, constr, EmailStr
from passlib.context import CryptContext
from citext import CIText

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(CIText, unique=True, index=True)
    email = Column(CIText, unique=True, index=True)
    hashed_password = Column(String)

    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
    collection = relationship("Collection", back_populates="user", cascade="all, delete-orphan")

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def set_password(self, password: str):
        self.hashed_password = self.pwd_context.hash(password)

    def verify_password(self, password: str):
        return self.pwd_context.verify(password, self.hashed_password)

class UserCreate(BaseModel):
    username: constr(regex=r'^[a-zA-Z0-9]{3,15}$')
    email: EmailStr
    password: constr(regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.,])[A-Za-z\d@$!%*?&.,]{8,20}$")

    @classmethod
    def validate_username(cls, username):
        return username.lower()

    @classmethod
    def validate_email(cls, email):
        return email.lower()
    
    #Other method of password validation
    # @classmethod
    # def validate_password(cls, password):
    #     # Check password complexity requirements
    #     if not re.match(
    #         r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$",
    #         password,
    #     ):
    #         raise ValidationError(
    #             "Password must be between 8 and 20 characters and contain at least "
    #             "1 upper and lower case letter, 1 number, and 1 special character."
    #         )
    #     return password

class UserResponse(BaseModel):
    id: int
    username: str
    email: str