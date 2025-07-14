from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, auth
from .db import SessionLocal, User, Note
from .auth import get_password_hash, verify_password, create_access_token, decode_access_token
from fastapi.security import OAuth2PasswordRequestForm

def get_db():
    """Yields DB session."""
    db_sess = SessionLocal()
    try:
        yield db_sess
    finally:
        db_sess.close()

router = APIRouter()

# PUBLIC_INTERFACE
@router.post("/auth/register", response_model=models.UserOut, summary="Register user")
def register_user(user: models.UserCreate, db: Session = Depends(get_db)):
    """Register a new user account."""
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    hashed = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return models.UserOut(id=db_user.id, email=db_user.email)

# PUBLIC_INTERFACE
@router.post("/auth/token", summary="Login and get access token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate user and issue JWT access token."""
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(token: str = Depends(auth.oauth2_scheme), db: Session = Depends(get_db)):
    user_id = decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# NOTES ROUTES

# PUBLIC_INTERFACE
@router.post("/notes", response_model=models.NoteOut, summary="Create a new note")
def create_note(note: models.NoteCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Create a new note for the authenticated user."""
    db_note = Note(title=note.title, content=note.content, user_id=current_user.id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

# PUBLIC_INTERFACE
@router.get("/notes", response_model=List[models.NoteOut], summary="List all notes")
def list_notes(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Fetch all notes belonging to the authenticated user."""
    return db.query(Note).filter(Note.user_id == current_user.id).order_by(Note.created_at.desc()).all()

# PUBLIC_INTERFACE
@router.get("/notes/{note_id}", response_model=models.NoteOut, summary="Get a note by ID")
def get_note(note_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Fetch a single note by ID for the authenticated user."""
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

# PUBLIC_INTERFACE
@router.put("/notes/{note_id}", response_model=models.NoteOut, summary="Update a note")
def update_note(note_id: int, note_update: models.NoteUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Update a note's title/content for the authenticated user."""
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note_update.title:
        note.title = note_update.title
    if note_update.content:
        note.content = note_update.content
    db.commit()
    db.refresh(note)
    return note

# PUBLIC_INTERFACE
@router.delete("/notes/{note_id}", summary="Delete a note")
def delete_note(note_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Delete a note owned by the authenticated user."""
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"ok": True}
