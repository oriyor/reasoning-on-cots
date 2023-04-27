class HoverEvaluator:
    @classmethod
    def create(cls, *args, **kwargs):
        return cls()

    def evaluate(self, pred: str, gold: str) -> str:
        pred = pred.lower().strip()
        if not (pred.startswith("yes") or pred.startswith("no")):
            return 0
        else:
            pred = "yes" if pred.startswith("yes") else "no"
        return 1 if pred.lower() == gold.lower() else 0
