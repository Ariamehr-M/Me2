from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, models
from .. import oauth2
from ..database import get_db
from ..repository import responses as responses_repo

router = APIRouter(
    prefix='/responses',
    tags=['Responses']
)

@router.post('/', response_model=schemas.ShowResponse)
def create_response(request: schemas.ResponseCreate, db: Session = Depends(get_db), current_user: schemas.ShowUser = Depends(oauth2.get_current_user)):
    return responses_repo.create_response(request, db)

@router.get('/pair/{pair_id}')
def get_pair_responses(pair_id: int, db: Session = Depends(get_db), current_user: schemas.ShowUser = Depends(oauth2.get_current_user)):
    return responses_repo.get_pair_responses(pair_id, db)

@router.get('/user/{respondent_id}', response_model=list[schemas.ShowResponse] )
def get_user_responses(respondent_id: int, db: Session = Depends(get_db), current_user: schemas.ShowUser = Depends(oauth2.get_current_user)):
    return responses_repo.get_user_responses(respondent_id, db)

@router.get('/pair/{pair_id}/overlap')
def get_overlap_responses(pair_id: int, db: Session = Depends(get_db), current_user: schemas.ShowUser = Depends(oauth2.get_current_user)):
    return responses_repo.get_overlap_responses(pair_id, db)
