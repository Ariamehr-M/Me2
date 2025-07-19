from fastapi import APIRouter, Depends
from .. import schemas
from .. import oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from ..repository import user as user_repo

router = APIRouter(
    prefix='/user',
     tags=['Users']
)



@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    return user_repo.create_user(request, db)

@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db), current_user: schemas.ShowUser = Depends(oauth2.get_current_user)):
    return user_repo.get_user(id, db)