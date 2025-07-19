from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status

def create_response(request: schemas.ResponseCreate, db: Session):
    new_response = models.Response(
        pair_id=request.pair_id,
        respondent_id=request.respondent_id,
        question_id=request.question_id,
        option_id=request.option_id
    )
    db.add(new_response)
    db.commit()
    db.refresh(new_response)
    return new_response

def get_pair_responses(pair_id: int, db: Session):
    pair = db.query(models.Pair).filter(models.Pair.id == pair_id).first()
    if not pair:
        return {"error": "Pair not found"}
    all_responses = db.query(models.Response).filter(models.Response.pair_id == pair_id).all()
    # Map: (question_id, respondent_id) -> option_id
    resp_map = {}
    for r in all_responses:
        resp_map[(r.question_id, r.respondent_id)] = r.option_id
    # Get all question_ids answered by either user
    question_ids = set(r.question_id for r in all_responses)
    result = []
    for qid in question_ids:
        user_a_response = resp_map.get((qid, pair.user_a_id))
        user_b_response = resp_map.get((qid, pair.user_b_id))
        result.append({
            "question_id": qid,
            "user_a_id": pair.user_a_id,
            "user_a_response": user_a_response,
            "user_b_id": pair.user_b_id,
            "user_b_response": user_b_response
        })
    return result
    return db.query(models.Response).filter(models.Response.pair_id == pair_id).all()

def get_user_responses(respondent_id: int, db: Session):
    return db.query(models.Response).filter(models.Response.respondent_id == respondent_id).all()

def get_overlap_responses(pair_id: int, db: Session):
    pair = db.query(models.Pair).filter(models.Pair.id == pair_id).first()
    if not pair:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Pair with id {pair_id} not found')
    responses = db.query(models.Response).filter(models.Response.pair_id == pair_id).all()
    # Group by question_id, option_id
    overlap = {}
    for r in responses:
        key = (r.question_id, r.option_id)
        overlap.setdefault(key, []).append(r.respondent_id)
    result = []
    for (question_id, option_id), respondent_ids in overlap.items():
        if pair.user_a_id in respondent_ids and pair.user_b_id in respondent_ids:
            result.append({'question_id': question_id, 'option_id': option_id})
    return result
