class EMEvaluator:
    @classmethod
    def create(cls, *args, **kwargs):
        return cls()

    def evaluate(self, pred: str, gold: str) -> str:
        if type(pred) == str and type(gold) == str:
            return 1 if pred.lower() == gold.lower() else 0
        return 1 if pred == gold else 0
