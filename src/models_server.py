import os
import cloudpickle
import lightgbm as lgb
import joblib

path = "src/models/"


# class Inferer:
#     def __init__(
#         self,
#         model: str,
#     ):
#         model_file = os.path.join(path, model)
#         self.inferer = joblib.load(open(model_file, "rb"))

#     def infer(self, df) -> int:
#         prediction = self.inferer.predict(df)
#         return prediction


class LgbInferer:
    def __init__(
        self,
        model: str,
    ):
        model_file = os.path.join(path, model)
        self.inferer = lgb.Booster(model_file=model_file)

    def infer(self, df) -> int:
        prediction = self.inferer.predict(df)
        prediction = 1 if prediction > 0.5 else 0
        return prediction


def model_pred(model, df):
    model_file = os.path.join(path, model)
    inferer = joblib.load(open(model_file, "rb"))
    prediction = inferer.predict(df)
    return int(prediction[0])
