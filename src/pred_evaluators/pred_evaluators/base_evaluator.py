class Evaluator:
    @classmethod
    def create(cls, *args, **kwargs):
        return cls()

    def evaluate(self, pred, gold) -> str:
        raise NotImplementedError("Please Implement this method")
