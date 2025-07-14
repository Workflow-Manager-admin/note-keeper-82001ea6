import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.sql import func
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# PUBLIC_INTERFACE
DB_URI = os.getenv("DATABASE_URL")
if not DB_URI:
    raise RuntimeError("DATABASE_URL is not set in the environment or .env file!")

engine = create_engine(DB_URI, connect_args={"check_same_thread": False} if "sqlite" in DB_URI else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base: DeclarativeMeta = declarative_base()

# PUBLIC_INTERFACE
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)

    notes = relationship("Note", back_populates="owner", cascade="all, delete-orphan")

# PUBLIC_INTERFACE
class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    owner = relationship("User", back_populates="notes")

# PUBLIC_INTERFACE
def init_db():
    """Initializes the database tables."""
    Base.metadata.create_all(bind=engine)
