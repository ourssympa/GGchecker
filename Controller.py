from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from  model import Url
from schema import UrlSchema, UrlCreate

router = APIRouter(
    tags=["urls"]
)

@router.get("/", response_model=List[UrlSchema])
def list_url (db: Session = Depends(get_db)):
    return db.query(Url).all()

@router.post("/", response_model=UrlCreate)
def create_url(request: UrlCreate, db: Session = Depends(get_db)):
    
    url_data = Url(
        url=request.url,
        status=request.status
    )
    db.add(url_data)
    db.commit()
    db.refresh(url_data)
    return url_data