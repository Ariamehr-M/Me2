from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text, SmallInteger, Index
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime
import uuid

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relationships
    sent_pairs = relationship('Pair', foreign_keys='Pair.user_a_id', back_populates='user_a')
    received_pairs = relationship('Pair', foreign_keys='Pair.user_b_id', back_populates='user_b')
    responses = relationship('Response', back_populates='respondent')

class Pair(Base):
    __tablename__ = 'pairs'
    id = Column(Integer, primary_key=True, index=True)
    user_a_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user_b_id = Column(Integer, ForeignKey('users.id'), nullable=True)  # can be null until user B registers
    invite_token = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relationships
    user_a = relationship('User', foreign_keys=[user_a_id], back_populates='sent_pairs')
    user_b = relationship('User', foreign_keys=[user_b_id], back_populates='received_pairs')
    responses = relationship('Response', back_populates='pair')
    __table_args__ = (Index('ix_pair_user_a_b', 'user_a_id', 'user_b_id'),)

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    question_type = Column(String, nullable=True)
    is_optional = Column(Boolean, default=False)
    position = Column(SmallInteger, nullable=True)
    group_id = Column(Integer, nullable=True)
    options = relationship('Option', back_populates='question')

class Option(Base):
    __tablename__ = 'options'
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    option = Column(Text, nullable=False)
    meaning_enum = Column(String, nullable=True)
    position = Column(SmallInteger, nullable=True)
    question = relationship('Question', back_populates='options')
    responses = relationship('Response', back_populates='option')

class Response(Base):
    __tablename__ = 'responses'
    id = Column(Integer, primary_key=True, index=True)
    pair_id = Column(Integer, ForeignKey('pairs.id'), nullable=False)
    respondent_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    option_id = Column(Integer, ForeignKey('options.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relationships
    pair = relationship('Pair', back_populates='responses')
    respondent = relationship('User', back_populates='responses')
    question = relationship('Question')
    option = relationship('Option', back_populates='responses')
    __table_args__ = (Index('ix_response_pair_respondent_question', 'pair_id', 'respondent_id', 'question_id'),)
