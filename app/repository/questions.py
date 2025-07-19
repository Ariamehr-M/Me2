from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status

def create_question(request: schemas.QuestionCreate, db: Session):
    new_question = models.Question(
        question=request.question,
        question_type=request.question_type,
        is_optional=request.is_optional,
        position=request.position,
        group_id=request.group_id
    )
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question

def get_question(question_id: int, db: Session):
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Question with id {question_id} not found')
    return question

def get_all_questions(db: Session):
    return db.query(models.Question).all()

def create_option(request: schemas.OptionCreate, db: Session):
    new_option = models.Option(
        question_id=request.question_id,
        option=request.option,
        meaning_enum=request.meaning_enum,
        position=request.position
    )
    db.add(new_option)
    db.commit()
    db.refresh(new_option)
    return new_option

def get_option(option_id: int, db: Session):
    option = db.query(models.Option).filter(models.Option.id == option_id).first()
    if not option:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Option with id {option_id} not found')
    return option

def get_options_for_question(question_id: int, db: Session):
    return db.query(models.Option).filter(models.Option.question_id == question_id).all()
