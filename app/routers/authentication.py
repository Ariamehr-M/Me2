from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, models
from ..database import get_db
from ..repository import user as user_repo
from ..hashing import Hash
from ..JWTtoken import create_access_token
from ..oauth2 import get_current_user

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

@router.post('/register', response_model=schemas.ShowUser)
def register(request: schemas.UserCreate, db: Session = Depends(get_db)):
    return user_repo.create_user(request, db)

@router.post('/login', response_model=schemas.Token)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user or not Hash.verify(user.password_hash, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
    


