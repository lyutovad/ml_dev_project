import src.models
from src.models import session, Prediction, UserModel, Credit, Model


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
