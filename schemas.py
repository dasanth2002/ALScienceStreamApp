from pydantic import BaseModel

class NoteBase(BaseModel):
    subject: str
    term: str
    content: str | None = None

class NoteCreate(NoteBase):
    pass

class NoteOut(NoteBase):
    id: int
    file_path: str | None

    class Config:
        orm_mode = True
