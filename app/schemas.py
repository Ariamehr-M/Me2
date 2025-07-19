from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    email: str
    name: str
    lastname: Optional[str] = None

class UserCreate(UserBase):
    password: str

class ShowUser(UserBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

# Pair Schemas
class PairBase(BaseModel):
    user_a_id: int
    user_b_id: Optional[int] = None

class PairCreate(PairBase):
    pass

class ShowPair(PairBase):
    id: int
    invite_token: str
    created_at: datetime
    class Config:
        from_attributes = True

# Question Schemas
class QuestionBase(BaseModel):
    question: str
    question_type: Optional[str] = None
    is_optional: Optional[bool] = False
    position: Optional[int] = None
    group_id: Optional[int] = None

class QuestionCreate(QuestionBase):
    pass

class ShowQuestion(QuestionBase):
    id: int
    options: List['ShowOption'] = []
    class Config:
        from_attributes = True

# Option Schemas
class OptionBase(BaseModel):
    question_id: int
    option: str
    meaning_enum: Optional[str] = None
    position: Optional[int] = None

class OptionCreate(OptionBase):
    pass

class ShowOption(OptionBase):
    id: int
    class Config:
        from_attributes = True

# Response Schemas
class ResponseBase(BaseModel):
    pair_id: int
    respondent_id: int
    question_id: int
    option_id: int

class ResponseCreate(ResponseBase):
    pass

class ShowResponse(ResponseBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

# Auth Schemas
class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

ShowQuestion.update_forward_refs()

