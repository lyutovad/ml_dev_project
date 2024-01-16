import os
import lightgbm as lgb


class LgbInferer:
    def __init__(
        self,
        path: str,
        model: str,
    ):
        model_file = os.path.join(path, model)
        self.inferer = lgb.load(filename=model_file)

    def infer(self, df) -> int:
        prediction = self.inferer.predict(df)
        return int(prediction)
