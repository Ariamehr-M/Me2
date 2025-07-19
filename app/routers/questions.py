from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas
from .. import oauth2
from ..database import get_db
from ..repository import questions as questions_repo

router = APIRouter(
    prefix='/questions',
    tags=['Questions']
)

@router.post('/', response_model=schemas.ShowQuestion)
def create_question(request: schemas.QuestionCreate, db: Session = Depends(get_db), current_user: schemas.ShowUser = Depends(oauth2.get_current_user)):
    return questions_repo.create_question(request, db)

@router.get('/{question_id}', response_model=schemas.ShowQuestion)
def get_question(question_id: int, db: Session = Depends(get_db)):
    return questions_repo.get_question(question_id, db)

@router.get('/', response_model=list[schemas.ShowQuestion])
def get_all_questions(db: Session = Depends(get_db)):
    return questions_repo.get_all_questions(db)

# Option endpoints
@router.post('/{question_id}/options', response_model=schemas.ShowOption)
def create_option(question_id: int, request: schemas.OptionCreate, db: Session = Depends(get_db), current_user: schemas.ShowUser = Depends(oauth2.get_current_user)):
    return questions_repo.create_option(request, db)

@router.get('/{question_id}/options', response_model=list[schemas.ShowOption])
def get_options_for_question(question_id: int, db: Session = Depends(get_db)):
    return questions_repo.get_options_for_question(question_id, db)

@router.get('/options/{option_id}', response_model=schemas.ShowOption)
def get_option(option_id: int, db: Session = Depends(get_db)):
    return questions_repo.get_option(option_id, db)
