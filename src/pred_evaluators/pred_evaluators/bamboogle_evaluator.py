from src.pred_evaluators.evaluation import compute_f1


class BamboogleEvaluator:
    @classmethod
    def create(cls, *args, **kwargs):
        return cls()

    def evaluate(self, pred: str, gold: str) -> str:
        return compute_f1(pred, gold)
