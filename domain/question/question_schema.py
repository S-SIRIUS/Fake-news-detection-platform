import datetime
from pydantic import BaseModel, validator
from domain.answer.answer_schema import Answer
class Question(BaseModel):
    id:int
    press: str | None=None
    content : str
    fake: float
    create_date: datetime.datetime
    answers: list[Answer] = []

    class Config:
        orm_mode=True
class QuestionList(BaseModel):

    total : int = 0
    question_list : list[Question]=[]
class QuestionCreate(BaseModel):
    press: str
    content: str

    @validator('press','content')
    def not_empty(cls,v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v