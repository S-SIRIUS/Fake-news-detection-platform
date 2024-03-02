from datetime import datetime

from domain.question.question_schema import QuestionCreate
from models import Question, User, Answer
from sqlalchemy.orm import Session
import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from transformers import AutoModel, AutoTokenizer, AutoModelForSequenceClassification
import torch
from torch.utils.data import Dataset, DataLoader
from keras.models import load_model
import joblib

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

"""
np.random.seed(42)
tf.random.set_seed(42)
train_tokenizer = joblib.load("domain/question/tokenizer.pkl") #tokenizer도 학습된거로 써야함
model_path = 'domain/question/FakeNewsTemp.h5'
model = load_model(model_path)
"""
#모델 가져오기 분류헤드가 아직 훈련되지 않았으니 오류는 정상
num_label = 2
model_ckpt="JKKANG/bert-fakenews"
model = (AutoModelForSequenceClassification.from_pretrained(model_ckpt, num_labels= num_label))
tokenizer = AutoTokenizer.from_pretrained(model_ckpt)
def create_question(db: Session, question_create: QuestionCreate):
    db_question = Question(press=question_create.press, content=question_create.content, fake=0,
                           create_date=datetime.now())
    """
    text=[db_question.content]
    maxlen = 500
    X = train_tokenizer.texts_to_sequences(text)
    X = pad_sequences(X, maxlen=maxlen, truncating='pre')
    prediction = (model.predict(X)) * 100  # Fake일 확룰
    print(prediction)
    """
    text = db_question.content
    inputs = tokenizer(text, return_tensors="pt")
    inputs = dict(inputs)
    with torch.no_grad():
        logits = outputs = model(**inputs).logits
    results = torch.softmax(logits, dim=1).tolist()[0]
    prediction=results[0]
    print(prediction)
    db_question.fake=prediction*100
    db.add(db_question)
    db.commit()
    Q_ID = db.query(Question).filter(Question.content==text).all()[0].id
    print(Q_ID)
    print(Q_ID)
    return {'value' : float(prediction)*100, 'idnum': int(Q_ID)}

def get_question(db:Session, question_id:int):
    question = db.query(Question).get(question_id)
    return question
def get_question_list(db: Session, skip: int = 0, limit: int = 10, keyword: str = ''):
    question_list = db.query(Question)
    if keyword:
        search = '%%{}%%'.format(keyword)
        sub_query = db.query(Answer.question_id, Answer.content, User.username) \
            .outerjoin(User, Answer.user_id == User.id).subquery()
        question_list = question_list \
            .outerjoin(User) \
            .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
            .filter(Question.press.ilike(search) |        # 언론사
                    Question.content.ilike(search) |        # 질문내용
                    User.username.ilike(search) |           # 질문작성자
                    sub_query.c.content.ilike(search) |     # 답변내용
                    sub_query.c.username.ilike(search)      # 답변작성자
                    )
    total = question_list.distinct().count()
    question_list = question_list.order_by(Question.create_date.desc())\
        .offset(skip).limit(limit).distinct().all()
    return total, question_list  # (전체 건수, 페이징 적용된 질문 목록)