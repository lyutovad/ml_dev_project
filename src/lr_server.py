import os
import cloudpickle


class Inferer:
    def __init__(
        self,
        path: str,
        model: str,
    ):
        model_file = os.path.join(path, model)
        with open(model_file, "rb") as file:
            self.inferer = cloudpickle.load(file)

    def infer(self, df) -> int:
        prediction = self.inferer.predict(df)
        return int(prediction)
