import os
from datetime import timedelta
from fastapi import FastAPI
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Annotated
from enum import Enum
from src.preprocess import Dataset
from src.lgb_server import LgbInferer
from src.lr_server import Inferer
import os
from dotenv import load_dotenv
from src.access_jwt import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    Token,
    User,
    get_current_active_user,
    create_access_token,
    authenticate_user,
    create_new_password,
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


class CalcModel(BaseModel):
    name_model: str
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


app = FastAPI(
    title="Классификация глиомы мозга",
    version="0.0.1",
    description="""""",
)

path_models = os.getenv("PATH_MODELS")


@app.get("/models_names")
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


# @app.get("/users/me/items/")
# async def read_own_items(
#     current_user: Annotated[User, Depends(get_current_active_user)]
# ):
#     return [{"item_id": "Foo", "owner": current_user.username}]


@app.get("/pass")
async def test_get_pass(pass_word: str):
    return create_new_password(pass_word)


@app.post("/calculate", response_model=User)
async def get_prediction(
    user_data: CalcModel,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return


# Счет пользователя:
# POST /api/deposit - Позволяет пользователю внести средства на счет.
# GET /api/ deposit - Возвращает текущий баланс счета пользователя (как разницу между всеми пополнениями и списаниями).

# Получение предсказания:
# GET /api/predict/{uid} – идентификатор предикта, который вернет uid предикта юзера
# POST /api/{name_model}/predict - Принимает данные от пользователя и возвращает предсказание в соответствии с выбранной моделью.

# История операций пользователя:
# GET /api/user_actions_history - Возвращает историю операций и действий пользователя, такие как пополнения счета, выбор моделей, списание средств и другие важные события.
