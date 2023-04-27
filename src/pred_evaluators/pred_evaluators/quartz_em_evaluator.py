class QuartzEMEvaluator:
    @classmethod
    def create(cls, *args, **kwargs):
        return cls()

    def evaluate(self, pred: str, gold: str) -> str:
        label_split = pred.split(".")[0].replace("\n", "")[:1]
        if len(label_split) == 0:
            return
        return label_split[0] == gold
