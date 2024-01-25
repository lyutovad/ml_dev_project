import pandas as pd
from datetime import datetime
from fastapi import HTTPException
from src.models import session, Prediction, User, Credit, Model, UserModel
from src.preprocess import preprocess, scaling
from src.models_server import LgbInferer, model_pred

mapping = {0: "LGG", 1: "GBM"}


def get_credits(userid):
    res = session.query(Credit).filter(Credit.user_id == userid).all()
    credits = 100
    for i in range(len(res)):
        if res[i].operation_type_id == 1:
            credits += res[i].amount
        elif res[i].operation_type_id == 2:
            credits -= res[i].amount
    return credits


def get_cost(modelid):
    res = session.query(Model).filter(Model.id == modelid).all()
    res = res[0].price
    return res


def validate_user(id, username):
    user = session.query(User).get(id)
    if user and user.username == username:
        return 1
    else:
        raise HTTPException(status_code=422, detail="Пользователь не найден")


def validate_data(id):
    data = session.query(Prediction).get(id)
    if data.result != -999:
        return 1
    else:
        raise HTTPException(status_code=422, detail="Запись не найдена")


def get_models_name(id):
    return session.query(Model).get(id).name


def make_prediction(id):
    data = session.query(Prediction).get(id)
    df = pd.DataFrame(
        [
            {
                "Years_at_diagnosis": data.Years_at_diagnosis,
                "Days_at_diagnosis": data.Days_at_diagnosis,
                "Gender": data.Gender,
                "Race": data.Race,
                "IDH1": data.IDH1,
                "TP53": data.TP53,
                "ATRX": data.ATRX,
                "PTEN": data.PTEN,
                "EGFR": data.EGFR,
                "CIC": data.CIC,
                "MUC16": data.MUC16,
                "PIK3CA": data.PIK3CA,
                "NF1": data.NF1,
                "PIK3R1": data.PIK3R1,
                "FUBP1": data.FUBP1,
                "RB1": data.RB1,
                "NOTCH1": data.NOTCH1,
                "BCOR": data.BCOR,
                "CSMD3": data.CSMD3,
                "SMARCA4": data.SMARCA4,
                "GRIN2A": data.GRIN2A,
                "IDH2": data.IDH2,
                "FAT4": data.FAT4,
                "PDGFRA": data.PDGFRA,
            }
        ]
    )
    df = preprocess(df)
    if data.model_id == 1:
        df = scaling(df)
    model = get_models_name(data.model_id)
    if data.model_id in [1, 2]:
        res = model_pred(model, df)
    else:
        inferer = LgbInferer(model=model)
        res = inferer.infer(df)
    return mapping[res], res


def record_calculation(dataid, userid, cost, res):
    prediction = session.query(Prediction).get(dataid)
    credits = Credit(
        user_id=userid, operation_type_id=2, amount=cost, data_prediction_id=dataid
    )
    try:
        prediction.result = res
        session.add(prediction)
        session.query(UserModel).filter(UserModel.data_id == dataid).update(
            {"used_on": datetime.now()}, synchronize_session="fetch"
        )
        session.add(credits)
        session.commit()
        return 1
    except Exception as e:
        session.rollback()
        return 0
