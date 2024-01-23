import os
from datetime import timedelta
from fastapi import FastAPI
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Annotated, Union
from enum import Enum
import os
import bcrypt
from dotenv import load_dotenv

from datetime import datetime
import uuid
import src.models
from src.models import session, Prediction, UserModel, Credit
from src.access_jwt import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    Token,
    User,
    get_current_active_user,
    create_access_token,
    authenticate_user,
    create_new_password,
)
from src.funks import (
    get_cost,
    get_credits,
    validate_user,
    validate_data,
    make_prediction,
)

load_dotenv()

MODELS_NAMES = {
    "lr_model": "Linear regression",
    "rf_model": "Random forest",
    "lgb_model": "LightGBM",
}


class App_Name(str, Enum):
    lr_model = "lr_model"
    rf_model = "rf_model"
    lgb_model = "lgb_model"


class GetData(BaseModel):
    Years_at_diagnosis: int
    Days_at_diagnosis: int
    Gender: str
    Race: str
    IDH1: str | None = "MUTATED"
    TP53: str | None = "MUTATED"
    ATRX: str | None = "MUTATED"
    PTEN: str | None = "MUTATED"
    EGFR: str | None = "MUTATED"
    CIC: str | None = "MUTATED"
    MUC16: str | None = "MUTATED"
    PIK3CA: str | None = "MUTATED"
    NF1: str | None = "MUTATED"
    PIK3R1: str | None = "MUTATED"
    FUBP1: str | None = "MUTATED"
    RB1: str | None = "MUTATED"
    NOTCH1: str | None = "MUTATED"
    BCOR: str | None = "MUTATED"
    CSMD3: str | None = "MUTATED"
    SMARCA4: str | None = "MUTATED"
    GRIN2A: str | None = "MUTATED"
    IDH2: str | None = "MUTATED"
    FAT4: str | None = "MUTATED"
    PDGFRA: str | None = "MUTATED"
    model_id: int | None = 1


class IdRecording(BaseModel):
    id: int | None


class Result(BaseModel):
    res: int


class Message(BaseModel):
    mes: str


class History(BaseModel):
    date: str
    id: int
    result: int
    credits: int


class UserData(BaseModel):
    username: str
    password: str
    email: str
    name: str
    surname: str


app = FastAPI(
    title="Классификация глиомы мозга",
    version="0.0.1",
    description="""""",
)

path_models = os.getenv("PATH_MODELS")


@app.post("/new_user", response_model=Message, tags=["User"])
async def get_data(
    new_user: UserData,
):
    """## Создать нового пользователя\n
    Returns:
    "mes": str
    """
    res = (
        session.query(src.models.User)
        .filter(src.models.User.username == new_user.username)
        .all()
    )
    if res:
        mes = Message(mes="Такой пользоватьль уже существует")
        return mes
    else:
        hashed_passw = bcrypt.hashpw(
            new_user.password.encode("utf-8"), bcrypt.gensalt()
        )
        user_line = src.models.User(
            username=new_user.username,
            password=hashed_passw,
            email=new_user.email,
            name=new_user.name,
            surname=new_user.surname,
            created_on=datetime.now(),
            updated_on=datetime.now(),
            disabled=False,
        )
        session.add(user_line)
        session.flush()
        credits_line = Credit(
            user_id=user_line.id,
            operation_type_id=3,
            amount=100,
        )
        session.add(credits_line)
        session.commit()
        response_message = Message(mes="Пользователь создан")
        return response_message


@app.get("/models_names", tags=["Data"])
def get_models_names():
    return MODELS_NAMES


# Authentication
@app.post("/token/", response_model=Token, tags=["Authentication"])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """## Получить токен\n
    Returns:
    "access_token": str
    "token_type": str
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/api/users/me/", response_model=User, tags=["Authentication"])
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """## Получить текущего пользователя\n"""
    return current_user


@app.post("/get_data", response_model=Union[IdRecording, Message], tags=["Data"])
async def get_data(
    user_data: GetData,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """## Получить данные для предсказания и номер модели\n
    Проверить, хватает ли средств \n
    Returns:
    "id": int |  "mes": str
    """
    data_line = Prediction(
        Years_at_diagnosis=user_data.Years_at_diagnosis,
        Days_at_diagnosis=user_data.Days_at_diagnosis,
        Gender=user_data.Gender,
        Race=user_data.Race,
        IDH1=user_data.IDH1,
        TP53=user_data.TP53,
        ATRX=user_data.ATRX,
        PTEN=user_data.PTEN,
        EGFR=user_data.EGFR,
        CIC=user_data.CIC,
        MUC16=user_data.MUC16,
        PIK3CA=user_data.PIK3CA,
        NF1=user_data.NF1,
        PIK3R1=user_data.PIK3R1,
        FUBP1=user_data.FUBP1,
        RB1=user_data.RB1,
        NOTCH1=user_data.NOTCH1,
        BCOR=user_data.BCOR,
        CSMD3=user_data.CSMD3,
        SMARCA4=user_data.SMARCA4,
        GRIN2A=user_data.GRIN2A,
        IDH2=user_data.IDH2,
        FAT4=user_data.FAT4,
        PDGFRA=user_data.PDGFRA,
        model_id=user_data.model_id,
    )

    session.add(data_line)
    session.flush()
    user_model_line = UserModel(
        user_id=current_user.id,
        model_id=user_data.model_id,
        data_id=data_line.id,
        uid=uuid.uuid1(),
    )
    session.add(user_model_line)
    session.commit()

    cost = get_cost(user_data.model_id)
    credits = get_credits(current_user.id)

    if cost < credits:
        return IdRecording(id=data_line.id)
    else:
        return Message(mes="Не хватает средств")


@app.post("/calculate", response_model=Union[IdRecording, Message], tags=["Data"])
async def get_data(
    dataid: IdRecording,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """## Выполнить расчеты, вернуть предсказание\n
    Проверить, существует ли пользователь\n
    Существует ли запись для предсказания, не отменена ли ранее\n
    Проверить, хватает ли средств\n
    Вызвать блок рассчета
    Returns:
    "mes": str
    """
    user = validate_user(current_user.id, current_user.username)
    data = validate_data(dataid.id)
    data_line = session.query(Prediction).get(dataid.id)
    cost = get_cost(data_line.model_id)
    credits = get_credits(current_user.id)
    money = 1 if credits > cost else 0
    if user + data + money == 3:
        result = make_prediction(dataid.id)
        return Message(mes=result)

    else:
        if not user:
            return Message(mes="Пользователь не найден")
        elif not data:
            return Message(mes="Данные не найдены")
        else:
            return Message(mes="Не хватает денег на операцию")


@app.put("/reject/{data_id}", response_model=Message, tags=["Data"])
async def get_data(
    data_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    ## Отказ от предсказания\n
    При отказе записать в результат предсказания -999
    "mes": str
    """
    data = session.query(Prediction).get(data_id)
    data.result = -999
    session.add(data)
    session.commit()
    return Message(mes="Запрос отменен")


@app.post("/history", response_model=History, tags=["User"])
async def get_data(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    ## История действий пользователя по диапазону дат\n
    """
    # вывести по диапазону дат историю
    pass


@app.post("/deposit", response_model=IdRecording, tags=["User"])
async def get_data(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    ## Получение баланса пользователя\n
    Returns:
    "credits": int
    """
    credits = get_credits(current_user.id)
    return IdRecording(id=credits)


@app.get("/refill", response_model=Message, tags=["User"])
async def get_data(
    credits: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    ## Пополнение баланса пользователя\n
    Returns:
    "mes": str
    """
    refill = Credit(user_id=current_user.id, operation_type_id=1, amount=credits)
    session.add(refill)
    session.commit()

    result = get_credits(current_user.id)
    message = f"Баланс пополнен. Текущий баланс = {result} credits"
    return Message(mes=message)


# @app.get("/pass", tags=["Authentication"])
# async def test_get_pass(pass_word: str):
#     return create_new_password(pass_word)


# @app.get("/users/me/items/")
# async def read_own_items(
#     current_user: Annotated[User, Depends(get_current_active_user)]
# ):
#     return [{"item_id": "Foo", "owner": current_user.username}]

# Счет пользователя:
# POST /api/deposit - Позволяет пользователю внести средства на счет.
# GET /api/ deposit - Возвращает текущий баланс счета пользователя (как разницу между всеми пополнениями и списаниями).
