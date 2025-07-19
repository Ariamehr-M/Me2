from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas
from .. import oauth2
from ..database import get_db
from ..repository import pair as pair_repo
from .. import models

router = APIRouter(
    prefix='/pairs',
    tags=['Pairs']
)

@router.post('/', response_model=schemas.ShowPair)
def create_pair(request: schemas.PairCreate, db: Session = Depends(get_db), current_user: schemas.ShowUser = Depends(oauth2.get_current_user)):
    return pair_repo.create_pair(request, db)

@router.get('/{pair_id}', response_model=schemas.ShowPair)
def get_pair(pair_id: int, db: Session = Depends(get_db), current_user: schemas.ShowUser = Depends(oauth2.get_current_user)):
    return pair_repo.get_pair(pair_id, db)

@router.get('/invite/{invite_token}', response_model=schemas.ShowPair)
def get_pair_by_invite_token(invite_token: str, db: Session = Depends(get_db)):
    return pair_repo.get_pair_by_invite_token(invite_token, db)

@router.post('/invite/{invite_token}/accept', response_model=schemas.ShowPair)
def accept_invite(
    invite_token: str,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(oauth2.get_current_user)
):
    user = db.query(models.User).filter(models.User.email == current_user.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return pair_repo.accept_invite(invite_token, user.id, db)

@router.get('/user/{user_id}', response_model=list[schemas.ShowPair])
def get_user_pairs(user_id: int, db: Session = Depends(get_db), current_user: schemas.ShowUser = Depends(oauth2.get_current_user)):
    return pair_repo.get_user_pairs(user_id, db)

@router.get('/', response_model=list[schemas.ShowPair])
def get_all_pairs(db: Session = Depends(get_db), current_user: schemas.ShowUser = Depends(oauth2.get_current_user)):
    return pair_repo.get_all_pairs(db)
