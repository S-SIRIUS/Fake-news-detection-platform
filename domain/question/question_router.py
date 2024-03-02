from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.question import question_crud, question_schema
router = APIRouter(
    prefix="/fakenews/question",
)


@router.post("/create")
def question_create(_question_create: question_schema.QuestionCreate, db: Session = Depends(get_db)):
    ans=question_crud.create_question(db=db, question_create=_question_create)

    return {"Fake":ans['value'], "Q_ID":ans['idnum']}

@router.get("/list",response_model=question_schema.QuestionList)
def question_list(db:Session=Depends(get_db),page: int = 0, size: int = 10, keyword: str = ''):
    total, _question_list = question_crud.get_question_list(db, skip=page * size, limit=size, keyword=keyword)
    return {
        'total': total,
        'question_list': _question_list
    }

@router.get("/detail/{question_id}", response_model=question_schema.Question)
def question_detail(question_id:int, db:Session=Depends(get_db)):
    question = question_crud.get_question(db, question_id=question_id)
    return question


