import os
import cloudpickle
import lightgbm as lgb

path = "src/models/"


class Inferer:
    path = "src/models/"

    def __init__(
        self,
        model: str,
    ):
        model_file = os.path.join(path, model)
        with open(model_file, "rb") as file:
            self.inferer = cloudpickle.load(file)

    def infer(self, df) -> int:
        prediction = self.inferer.predict(df)
        return int(prediction)


class LgbInferer:
    def __init__(
        self,        
        model: str,
    ):
        model_file = os.path.join(model)
        self.inferer = lgb.load(filename=model_file)

    def infer(self, df) -> int:
        prediction = self.inferer.predict(df)
        return int(prediction)
