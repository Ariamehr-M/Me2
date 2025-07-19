from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status

def create_pair(request: schemas.PairCreate, db: Session):
    new_pair = models.Pair(user_a_id=request.user_a_id, user_b_id=request.user_b_id)
    db.add(new_pair)
    db.commit()
    db.refresh(new_pair)
    return new_pair

def get_pair(pair_id: int, db: Session):
    pair = db.query(models.Pair).filter(models.Pair.id == pair_id).first()
    if not pair:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Pair with id {pair_id} not found')
    return pair

def get_pair_by_invite_token(invite_token: str, db: Session):
    pair = db.query(models.Pair).filter(models.Pair.invite_token == invite_token).first()
    if not pair:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Pair with invite_token {invite_token} not found')
    return pair



def accept_invite(invite_token: str, user_b_id: int, db: Session):
    pair = db.query(models.Pair).filter(models.Pair.invite_token == invite_token).first()
    if not pair:
        raise HTTPException(status_code=404, detail="Pair not found")
    if pair.user_b_id is not None:
        raise HTTPException(status_code=400, detail="Pair already accepted")
    pair.user_b_id = user_b_id
    db.commit()
    db.refresh(pair)
    return pair





def get_user_pairs(user_id: int, db: Session):
    pairs = db.query(models.Pair).filter(
        (models.Pair.user_a_id == user_id) | (models.Pair.user_b_id == user_id)
    ).all()
    return pairs

def get_all_pairs(db: Session):
    return db.query(models.Pair).all()
