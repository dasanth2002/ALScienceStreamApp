from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models.notes_model import Note
from fastapi.responses import FileResponse
import os
import shutil

router = APIRouter()


# Ensure upload folder exists
UPLOAD_DIR = "uploaded_notes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/materials/notes/upload_pdf/")
async def upload_pdf(subject: str, term: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    filename = f"{subject}_{term}_{file.filename}".replace(" ", "_")

 # Duplicate check - இதே file ஏற்கனவே இருக்கிறதா என்று பார்த்துக் கொள்ளும்
    existing_note = db.query(Note).filter(Note.subject == subject, Note.term == term, Note.file_path == filename).first()
    if existing_note:
        raise HTTPException(status_code=400, detail="This file already uploaded.")




    file_location = os.path.join(UPLOAD_DIR, filename)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    note = Note(subject=subject, term=term, file_path=filename)
    db.add(note)
    db.commit()
    db.refresh(note)
    return {
        "id": note.id,
        "subject": note.subject,
        "term": note.term,
        "file_path": note.file_path,
    }


@router.get("/materials/notes/list/{subject}/{term}")
def get_notes(subject: str, term: str, db: Session = Depends(get_db)):
    notes = db.query(Note).filter(Note.subject == subject, Note.term == term).all()
    return notes

@router.get("/materials/notes/download/{filename}")
def download_pdf(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file_path, media_type='application/pdf', filename=filename)


