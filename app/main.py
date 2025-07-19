from fastapi import FastAPI
from .routers import user, authentication, pair, questions, responses
from . import models
from .database import engine

app = FastAPI()


models.Base.metadata.create_all(bind=engine)


app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(pair.router)
app.include_router(questions.router)
app.include_router(responses.router)



