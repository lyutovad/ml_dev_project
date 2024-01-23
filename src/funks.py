import pandas as pd
from src.models import session, Prediction, User, Credit, Model
from src.preprocess import Dataset
from src.models_server import Inferer, LgbInferer

mapping = {0: "NOT_MUTATED", 1: "MUTATED"}


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
    return True if user.username == username else False


def validate_data(id):
    data = session.query(Prediction).get(id)
    return False if not data or data.result == -999 else True


def get_models_name(id):
    return session.query(Model).get(id).name


def make_prediction(id):
    data = session.query(Prediction).get(id)
    df = pd.DataFrame(
        columns={
            "Years_at_diagnosis": data.Years_at_diagnosis,
            "Days_at_diagnosis": data.Days_at_diagnosis,
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
    )
    data_df = Dataset(df=df)
    data_df.preprocess()
    if data.model_id == 1:
        data_df.scaling()
    model = get_models_name(data.model_id)
    if data.model_id in [1, 2]:
        inferer = Inferer(model=model)
        inferer.infer()
    else:
        inferer = LgbInferer(model=model)
        inferer.infer()
    return mapping[inferer.infer()]
